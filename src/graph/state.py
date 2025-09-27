from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class AgentSignal(BaseModel):
    action: str
    confidence: float

class FinalOrder(BaseModel):
    action: str
    size: int

class AgentState(BaseModel):
    ticker: str
    price: float = 0.0
    signals: Dict[str, str] = {} #Agent-Name -> "buy/sell/hold"
    reasoning: Dict[str, str] = {} #Agent-Name -> "reasoning"
     # NEW: single-agent recommendation
    agent_signal: AgentSignal = None

    # downstream fields
    risk: Dict[str, Optional[float]] = Field(default_factory=dict)
    final_order: FinalOrder = None
    metrics: Dict[str, float] = Field(default_factory=dict)

    # portfolio context
    portfolio_value: float = 0.0
    cash: float = 0.0
    holdings: int = 0

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True