from typing import TypedDict, List, Dict, Any
from typing_extensions import Annotated
from operator import add

class StartupState(TypedDict):
    idea: str
    
    market_analysis: str
    competitor_analysis: str
    swot_analysis: str
    financial_risk_analysis: str

    market_score: int

    investment_score: float
    final_decision: str

    messages: Annotated[List[Dict[str, Any]], add]