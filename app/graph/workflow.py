from langgraph.graph import StateGraph
from app.graph.state import StartupState
from app.agents.market_agent import market_agent

def create_workflow():

    graph = StateGraph(StartupState)

    # Add node
    graph.add_node("market_analysis", market_agent)

    # Define entry point
    graph.set_entry_point("market_analysis")

    # Define end point
    graph.set_finish_point("market_analysis")

    return graph.compile()