from pydantic import BaseModel, conint, constr
from datetime import datetime
from enum import Enum
from typing import Optional


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



class SearchFilter(BaseModel):
    name_regex: Optional[constr(strip_whitespace=True)] 
    min_active_count: Optional[conint(ge=0)] 
    start_time_from: Optional[datetime] 
    start_time_to: Optional[datetime] 
    timezone: Optional[str]  

class SearchModel(BaseModel):
    sport: Optional[SearchFilter]
    event: Optional[SearchFilter]
    selection: Optional[SearchFilter]
