import time
from langchain_core.prompts import ChatPromptTemplate
from app.rag.rag_pipeline import build_rag_chain
from app.llm import get_llm
from app.rag.vector_store import load_vectorstore

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever()

def swot_agent(state):
    print("SWOT Agent is analyzing...")
    print("⏳ Waiting 5 seconds...")
    time.sleep(5)
    
    # Safely get the context gathered by previous agents
    idea = state.get("idea", "")
    market = state.get("market_analysis", "")
    competitors = state.get("competitor_analysis", "")

    rag_chain = build_rag_chain(retriever)

    rag_data = rag_chain.invoke({
        "query": idea
    })

    context = rag_data["context"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite Startup Strategy Analyst. 
        Read the provided startup idea, market analysis, and competitor research carefully.

        Use the following internal knowledge when relevant:
        {context}
        
        You MUST format your final response exactly with these four headings:
        - Strengths
        - Weaknesses
        - Opportunities
        - Threats
        
        Keep your points concise, analytical, and directly tied to the provided market/competitor data.
        If the provided market or competitor context is empty or says 'no results', do NOT invent data. State clearly that you cannot complete the analysis due to missing upstream data
        """),
        
        ("human", "Idea: {idea}\n\nMarket: {market}\n\nCompetitors: {competitors}\n\nPlease generate the SWOT analysis.")
    ])
    
    llm = get_llm()
    chain = prompt | llm
    response = chain.invoke({
        "idea": idea, 
        "market": market, 
        "competitors": competitors,
        "context": context
    })
    
    # ✅ FIX: Grab .content directly! No dictionary indexing here.
    raw_content = response.content
    
    # 🧹 CLEANUP: If Gemini returned a complex list with a signature, just grab the text!
    if isinstance(raw_content, list):
        final_answer = raw_content[0]["text"]
    else:
        final_answer = raw_content
    
    return {"swot_analysis": final_answer}