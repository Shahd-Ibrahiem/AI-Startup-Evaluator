from app.graph.workflow import create_workflow

from dotenv import load_dotenv
load_dotenv()

def main():
    workflow = create_workflow()

    initial_state = {
        "idea": "AI-powered fitness startup",
        "market_analysis": "",
        "competitor_analysis": "",
        "swot_analysis": "",
        "financial_risk_analysis": "",
        "investment_score": 0,
        "final_decision": "",
        "messages": []
    }

    #result = workflow.invoke(initial_state)

    result = workflow.invoke(initial_state,
    config={
        "configurable": {
            "thread_id": "startup_evaluator_1"
        }
    })


    print("\n===== MARKET ANALYSIS =====\n")
    print(result["market_analysis"])

    print("\n===== COMPETITORS ANALYSIS =====\n")
    print(result["competitor_analysis"])

    print("\n===== SWOT ANALYSIS =====\n")
    print(result["swot_analysis"])

    print("\n===== FINANCIAL RISK ANALYSIS =====\n")
    print(result["financial_risk_analysis"])

    print("\n===== FINAL DECISION =====")
    print(result["final_decision"])

    #print(result)

if __name__ == "__main__":
    main()