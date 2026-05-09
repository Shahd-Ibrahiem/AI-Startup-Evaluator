from app.llm import get_llm

def competitor_agent(state):
    llm = get_llm()

    prompt = f"""
    You are a startup analyst.

    Analyze competitors for this idea:
    {state["idea"]}

    Provide:
    - Direct competitors
    - Indirect competitors
    - Market saturation level
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "competitor_analysis": response.content
    }