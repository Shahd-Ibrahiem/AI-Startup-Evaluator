from app.graph.workflow import create_workflow



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

   # result = workflow.invoke(initial_state)
    # <-- ADD THIS CONFIG DICTIONARY -->
    config = {"configurable": {"thread_id": "startup-eval-thread-1"}}

    # <-- PASS THE CONFIG TO INVOKE -->
    result = workflow.invoke(initial_state, config=config)

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