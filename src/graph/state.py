from typing import Dict, List, Optional
from pydantic import BaseModel

class AgentState(BaseModel):
    ticker: str
    price: float = 0.0
    signals: Dict[str, str] = {} #Agent-Name -> "buy/sell/hold"
    reasoning: Dict[str, str] = {} #Agent-Name -> "reasoning"