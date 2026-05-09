from app.llm import get_llm

def market_agent(state):
    llm = get_llm()

    prompt = f"""
    You are a market research analyst.
    Analyze this startup idea:

    {state["idea"]}

    Provide:
    - Market potential
    - Target customers
    - Growth opportunity
    """

    # simple heuristic
    score = 70

    response = llm.invoke(prompt)

    # simple heuristic
    score = 70

    return {
        **state,
        "market_analysis": response.content,
        "market_score": score
    }