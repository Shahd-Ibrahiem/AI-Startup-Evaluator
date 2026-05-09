from app.llm import get_llm

def financial_agent(state):
    llm = get_llm()

    prompt = f"""
    You are a financial risk analyst.

    Startup idea:
    {state["idea"]}

    Market:
    {state["market_analysis"]}

    Competitors:
    {state["competitor_analysis"]}

    SWOT:
    {state["swot_analysis"]}

    Analyze:
    - Cost structure
    - Revenue potential
    - Risks
    - Profit feasibility

    Return analysis and a risk level (Low / Medium / High)
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "financial_risk_analysis": response.content
    }