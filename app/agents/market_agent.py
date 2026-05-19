from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from app.llm import get_llm
from app.utils.scoring import extract_score
from app.rag.rag_pipeline import build_rag_chain
import time
from dotenv import load_dotenv
load_dotenv()

from app.rag.vector_store import load_vectorstore

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever()

# 1. Initialize the Search Tool properly
web_search_tool = TavilySearch(max_results=3)
tools = [web_search_tool]

# 2. Create the ReAct agent (This automatically handles the tool-calling loop!)
llm = get_llm()
agent = create_react_agent(llm, tools)

def market_agent(state):
    print("Market Agent is researching...")
    print("⏳ Waiting 5 seconds...")
    time.sleep(5)
    
    # Safely get the idea
    idea = state.get("idea", "")

    rag_chain = build_rag_chain(retriever)

    rag_data = rag_chain.invoke({
        "query": idea
    })

    context = rag_data["context"]
    
    # Combine Code 1's role with Code 2's specific formatting
    system_prompt = f"""You are an expert Market Research Analyst.

    You MUST use your web search tool.

    Relevant Internal Knowledge:
    {context}

    Scoring Rules:
    - Give scores BELOW 50 for outdated, low-demand, impractical, unrealistic, or obsolete business ideas.
    - Give scores BETWEEN 50 and 70 for average or uncertain ideas.
    - Give scores ABOVE 70 only for highly scalable, modern, high-demand startup ideas.

    Examples of LOW scoring ideas:
    - DVD rental businesses
    - Printed map navigation businesses
    - Fax machine services
    - CD delivery startups
    Be strict and realistic. Do NOT inflate scores.

    Format your final analysis exactly with these headings:
    - Market Potential
    - Target Customers
    - Growth Opportunity
    - Market Score: [Provide a score from 0 to 100 in format X/100]
    """
    
    user_prompt = f"Analyze the market for this startup idea: {idea}"
    
    # Invoke the ReAct agent
    response = agent.invoke({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]})
    
    # 1. Dig into the dictionary and get the content of the LAST message
    raw_content = response["messages"][-1].content
    
    # 2. 🧹 CLEANUP: If Gemini returned a complex list with a signature, grab just the text
    if isinstance(raw_content, list):
        final_answer = raw_content[0]["text"]
    else:
        final_answer = raw_content

    # 3. Safely extract the score using our try-except block
    try:
        score = extract_score(final_answer)
    except Exception as e:
        print(f"⚠️ Failed to extract exact market score: {e}. Defaulting to 0.")
        score = 0
    
    # 4. Return the clean data to the main state
    return {
        "market_analysis": final_answer,
        "market_score": score
    }