from typing import TypedDict, List, Dict, Any

class StartupState(TypedDict):
    idea: str
    
    market_analysis: str
    competitor_analysis: str
    swot_analysis: str
    financial_risk_analysis: str

    market_score: int

    investment_score: float
    final_decision: str

    messages: List[Dict[str, Any]]