from typing import TypedDict, List, Dict, Any

class StartupState(TypedDict):
    idea: str
    analysis: str
    messages: List[Dict[str, Any]]