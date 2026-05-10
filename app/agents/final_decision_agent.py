import time
from langchain_core.prompts import ChatPromptTemplate
from app.llm import llm
from app.utils.scoring import extract_score

def final_decision_agent(state):
    print("Final Decision Agent is making the call...")
    print("⏳ Waiting 15 seconds to respect Google's free tier limits...")
    time.sleep(15)
    
    # Safely get data from state
    idea = state.get("idea", "")
    market = state.get("market_analysis", "")
    competitors = state.get("competitor_analysis", "")
    swot = state.get("swot_analysis", "")
    financial = state.get("financial_risk_analysis", "")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite venture capital Final Decision Agent. 
        Review the gathered data and output a final evaluation.
        
        You MUST format your response exactly like this:
        1. Investment Score: [Provide a score from 0 to 100, format: X/100]
        2. Decision: [Exactly 'Invest', 'Consider', or 'Avoid']
        3. Reasoning: [Provide a 3-4 sentence justification]
        
        If the provided market or competitor context is empty or says 'no results', do NOT invent data. State clearly that you cannot complete the analysis due to missing upstream data
        """),
        ("human", "Idea: {idea}\n\nMarket: {market}\n\nCompetitors: {competitors}\n\nSWOT: {swot}\n\nFinancial Risk: {financial}\n\nWhat is your final decision?")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "idea": idea, 
        "market": market, 
        "competitors": competitors,
        "swot": swot,
        "financial": financial
    })
    
    # ✅ FIX: Grab .content directly! No dictionary indexing here.
    raw_content = response.content
    
    # 🧹 CLEANUP
    if isinstance(raw_content, list):
        final_answer = raw_content[0]["text"]
    else:
        final_answer = raw_content
        
    # ✅ FIX: Add the Try-Except block so the whole app doesn't crash if the score extraction fails
    try:
        score = extract_score(final_answer)
    except Exception as e:
        print(f"⚠️ Failed to extract exact score: {e}. Defaulting to 0.")
        score = 0
    
    return {
        "final_decision": final_answer,
        "investment_score": score
    }