from app.llm import get_llm

def swot_agent(state):
    llm = get_llm()

    prompt = f"""
    You are a startup strategy analyst.

    Based on this startup idea:
    {state["idea"]}

    Market Analysis:
    {state["market_analysis"]}

    Competitors:
    {state["competitor_analysis"]}

    Generate a SWOT analysis:
    - Strengths
    - Weaknesses
    - Opportunities
    - Threats
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "swot_analysis": response.content
    }