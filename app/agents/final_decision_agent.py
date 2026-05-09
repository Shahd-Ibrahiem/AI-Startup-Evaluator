from app.llm import get_llm

def final_decision_agent(state):
    llm = get_llm()

    prompt = f"""
    You are an investment decision system.

    Based on:

    Market:
    {state["market_analysis"]}

    Competitors:
    {state["competitor_analysis"]}

    SWOT:
    {state["swot_analysis"]}

    Financial Risk:
    {state["financial_risk_analysis"]}

    TASK:
    1. Give investment score (0–100)
    2. Decide: Invest / Consider / Reject
    3. Explain reasoning
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "final_decision": response.content,
        "investment_score": 0  # we can extract later
    }