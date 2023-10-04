from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class EventType(Enum):
    PREPLAY = "preplay"
    INPLAY = "inplay"


class EventStatus(Enum):
    STARTED = "started"
    PENDING = "pending"
    ENDED = "ended"
    CANCELLED = "cancelled"

class SportBase(BaseModel):
    name: str
    slug: str
    active: bool

class EventBase(BaseModel):
    name: str
    slug: str
    active: bool
    type: EventType  
    status: EventStatus
    sport_id: int
    scheduled_start: datetime
    actual_start: datetime

class SelectionOutcome(Enum):
    UNSETTLED = "unsettled"
    VOID = "void"
    LOSE = "lose"
    WIN = "win"

class SelectionBase(BaseModel):
    name: str
    event_id: int
    price: float
    active: bool
    outcome: SelectionOutcome

