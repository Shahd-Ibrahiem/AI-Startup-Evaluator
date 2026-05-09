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

    response = llm.invoke(prompt)

    state["analysis"] = response.content

    return state