import time
from langchain_core.prompts import ChatPromptTemplate
from app.rag.rag_pipeline import build_rag_chain
from app.llm import get_llm
from app.utils.scoring import extract_score

from app.rag.vector_store import load_vectorstore

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever()

def final_decision_agent(state):
    print("Final Decision Agent is making the call...")
    print("⏳ Waiting 5 seconds...")
    time.sleep(5)
    
    # Safely get data from state
    idea = state.get("idea", "")
    market = state.get("market_analysis", "")
    competitors = state.get("competitor_analysis", "")
    swot = state.get("swot_analysis", "")
    financial = state.get("financial_risk_analysis", "")

    rag_chain = build_rag_chain(retriever)

    rag_data = rag_chain.invoke({
        "query": idea
    })

    context = rag_data["context"]

    market_score = state.get("market_score", 0)

    if market_score < 50:
        return {
            "final_decision": """
            1. Investment Score: 20/100
            2. Decision: Avoid
            3. Reasoning: The startup idea showed weak market potential during the initial market analysis stage. The workflow automatically terminated early to avoid unnecessary deep analysis due to low market viability.
            """,
        "investment_score": 20
        }
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite venture capital Final Decision Agent. 
        Review the gathered data and output a final evaluation.
        
        Use the following internal knowledge when relevant:
        {context}

        You MUST format your response exactly like this:
        1. Investment Score: [Provide a score from 0 to 100, format: X/100]
        2. Decision: [Exactly 'Invest', 'Consider', or 'Avoid']
        3. Reasoning: [Provide a 3-4 sentence justification]
        
        If the provided market or competitor context is empty or says 'no results', do NOT invent data. State clearly that you cannot complete the analysis due to missing upstream data
        """),
        ("human", "Idea: {idea}\n\nMarket: {market}\n\nCompetitors: {competitors}\n\nSWOT: {swot}\n\nFinancial Risk: {financial}\n\nWhat is your final decision?")
    ])
    
    llm = get_llm()
    chain = prompt | llm
    response = chain.invoke({
        "idea": idea, 
        "market": market, 
        "competitors": competitors,
        "swot": swot,
        "financial": financial,
        "context": context
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