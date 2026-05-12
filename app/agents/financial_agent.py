from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from app.llm import get_llm
import time

from app.rag.vector_store import load_vectorstore

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever()

# 1. Keep the Search Tool so it can look up real prices!
web_search_tool = TavilySearch(max_results=3)
tools = [web_search_tool]
llm = get_llm()
agent = create_react_agent(llm, tools)

def financial_agent(state):
    print("Financial Agent is crunching numbers...")
    print("⏳ Waiting 5 seconds...")
    time.sleep(5)
    
    # 2. Safely get ALL the context like Code 2 did
    idea = state.get("idea", "")
    market = state.get("market_analysis", "")
    competitors = state.get("competitor_analysis", "")
    swot = state.get("swot_analysis", "")

    docs = retriever.invoke(idea)

    context = "\n\n".join([d.page_content for d in docs])
    
    # 3. Combine Code 1's role with Code 2's specific output format
    system_prompt = """You are an expert Financial Risk Analyst. 
    Use your web search tool to look up real, current costs, pricing models, and financial risks for this specific type of business.
    
    Use the following internal knowledge when relevant:
    {context}

    Your final report MUST be structured with these exact headings:
    - Cost Structure (Based on real current market prices)
    - Revenue Potential
    - Financial Risks
    - Profit Feasibility
    - Overall Risk Level: [Strictly write: Low, Medium, or High]"""
    
    user_prompt = f"Idea: {idea}\n\nMarket: {market}\n\nCompetitors: {competitors}\n\nSWOT: {swot}\n\nPlease research and evaluate the financial feasibility."
    
    # 4. Run the modern ReAct agent
    response = agent.invoke({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]})
    
    
    
    # Extract the final answer
    raw_content = response["messages"][-1].content
    
    # 🧹 CLEANUP: If Gemini returned a complex list with a signature, just grab the text!
    if isinstance(raw_content, list):
        final_answer = raw_content[0]["text"]
    else:
        final_answer = raw_content
    
    return {"financial_risk_analysis": final_answer} # (Make sure the key matches the agent!)
    
    
