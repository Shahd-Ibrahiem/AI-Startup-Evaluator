from langgraph.graph import StateGraph
from app.graph.state import StartupState
from app.agents.market_agent import market_agent
from app.agents.competitor_agent import competitor_agent

def create_workflow():

    graph = StateGraph(StartupState)

    # Add node
    graph.add_node("market_analysis", market_agent)
    graph.add_node("competitor_analysis", competitor_agent)

    # Define entry point
    graph.set_entry_point("market_analysis")
    graph.add_edge("market_analysis", "competitor_analysis")

    # Define end point
    graph.set_finish_point("competitor_analysis")

    return graph.compile()
