from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    query: str
    context: Optional[List[str]]
    route: Optional[str]
    retry: Optional[bool]
    answer: Optional[str]
    