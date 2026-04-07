from pydantic import BaseModel, Field, conlist
from typing import List, Optional, Dict, Any
from enum import Enum

class Classification(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Action(BaseModel):
    classification: Dict[int, Classification] = {}
    response: Dict[int, str] = {}
    priority_order: Optional[List[int]] = None

class Email(BaseModel):
    id: int
    subject: str
    body: str
    sender: str

class Observation(BaseModel):
    emails: List[Email]
    current_task: str
    task_progress: str = ""

class Reward(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    feedback: str

class State(BaseModel):
    emails: List[Email]
    task: str
    progress: str
    step_count: int = 0
    actions_history: List[Dict[str, Any]] = []

