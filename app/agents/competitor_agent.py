import time
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from app.llm import get_llm

# 1. Initialize the Search Tool
web_search_tool = TavilySearch(max_results=3)
tools = [web_search_tool]

# 2. Create the native LangGraph agent
llm = get_llm()
agent = create_react_agent(llm, tools)

def competitor_agent(state):
    print("Competitor Agent is researching...")
    print("⏳ Waiting 15 seconds to respect Google's free tier limits...")
    time.sleep(15)
    
    # Safely get context from previous steps
    idea = state.get("idea", "")
    market_analysis = state.get("market_analysis", "")
    
    # Combine Code 1's tools with Code 2's specific formatting
    system_prompt = """You are an expert Competitor Analysis Agent. 
    You MUST use your web search tool to find real, current companies that compete directly or indirectly with this startup idea.
    
    Format your final report exactly with these headings:
    - Direct Competitors (Name the specific companies and what they do)
    - Indirect Competitors (Name the specific companies)
    - Market Saturation Level (Evaluate how crowded this specific space is)"""
    
    user_prompt = f"Startup Idea: {idea}\n\nMarket Context: {market_analysis}\n\nPlease analyze the competitors."
    
    # Invoke the agent
    response = agent.invoke({"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]})
    
    # Extract the final answer
    # Extract the final answer
    raw_content = response["messages"][-1].content
    
    # 🧹 CLEANUP: If Gemini returned a complex list with a signature, just grab the text!
    if isinstance(raw_content, list):
        final_answer = raw_content[0]["text"]
    else:
        final_answer = raw_content
    
    return {"competitor_analysis": final_answer} # (Make sure the key matches the agent!)