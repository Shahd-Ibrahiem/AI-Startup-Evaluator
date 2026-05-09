from app.graph.workflow import create_workflow

def main():
    workflow = create_workflow()

    initial_state = {
        "idea": "AI-powered fitness startup",
        "analysis": "",
        "messages": []
    }

    result = workflow.invoke(initial_state)

    print("\n===== MARKET ANALYSIS =====\n")
    print(result["analysis"])

if __name__ == "__main__":
    main()