from langgraph.graph import StateGraph
from app.graph.state import StartupState
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from app.agents.market_agent import market_agent
from app.agents.competitor_agent import competitor_agent
from app.agents.swot_agent import swot_agent
from app.agents.financial_agent import financial_agent
from app.agents.final_decision_agent import final_decision_agent


def route_after_market(state):
    score = state.get("market_score", 50)

    if score < 50:
        return "final_decision"
    return "competitor_analysis"


def create_workflow():

    graph = StateGraph(StartupState)

    # Add node
    graph.add_node("market_analysis", market_agent)
    graph.add_node("competitor_analysis", competitor_agent)
    graph.add_node("swot_analysis", swot_agent)
    graph.add_node("financial_risk_analysis", financial_agent)
    graph.add_node("final_decision", final_decision_agent)

    # Define entry point
    graph.set_entry_point("market_analysis")

    graph.add_conditional_edges(
        "market_analysis",
        route_after_market,
        {
            "competitor_analysis": "competitor_analysis",
            "final_decision": "final_decision"
        }
    )

    # Normal flow after competitors
    graph.add_edge("competitor_analysis", "swot_analysis")
    graph.add_edge("swot_analysis", "financial_risk_analysis")
    graph.add_edge("financial_risk_analysis", "final_decision")

    # Define end point
    graph.set_finish_point("final_decision")
    
    # <-- NEW PERMANENT MEMORY -->
    # This creates a physical file named "checkpoints.db" in your folder to save everything forever
    conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
    memory = SqliteSaver(conn)
    return graph.compile(checkpointer=memory)

