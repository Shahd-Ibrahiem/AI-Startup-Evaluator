from app.llm import get_llm
from app.utils.scoring import extract_score

def final_decision_agent(state):
    llm = get_llm()

    prompt = f"""
    You are an investment decision system.

    Provide:
    1. Investment score (0–100 format: X/100)
    2. Decision: Invest / Consider / Reject
    3. Reasoning

    Idea:
    {state["idea"]}

    Market:
    {state["market_analysis"]}

    Competitors:
    {state["competitor_analysis"]}

    SWOT:
    {state["swot_analysis"]}

    Financial:
    {state["financial_risk_analysis"]}
    """

    response = llm.invoke(prompt)

    score = extract_score(response.content)

    return {
        **state,
        "final_decision": response.content,
        "investment_score": score
    }