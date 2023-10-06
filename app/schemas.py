from pydantic import BaseModel, conint, constr
from datetime import datetime
from enum import Enum
from typing import Optional


class EventType(Enum):
    PREPLAY = "preplay"
    INPLAY = "inplay"


class EventStatus(Enum):
    PENDING = "pending"
    STARTED = "started"
    ENDED = "ended"
    CANCELLED = "cancelled"

class EventUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    active: Optional[bool] = None
    type: Optional[EventType] = None
    sport_id: Optional[int] = None
    status: Optional[EventStatus] = None
    scheduled_start: Optional[datetime] = None
    actual_start: Optional[datetime] = None


class EventBase(BaseModel):
    name: str
    slug: str
    active: bool
    type: EventType  
    status: EventStatus
    sport_id: int
    scheduled_start: datetime
    actual_start: datetime



class SportBase(BaseModel):
    name: str
    slug: str
    active: bool

class SportUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    active: Optional[bool] = None


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

class SelectionUpdate(BaseModel):
    name: Optional[str] = None
    event_id: Optional[int] = None
    price: Optional[float] = None
    active:  Optional[bool] = None
    outcome: Optional[SelectionOutcome] = None

class SearchFilter(BaseModel):
    name_regex: Optional[constr(strip_whitespace=True)] 
    min_active_count: Optional[conint(ge=0)] 
    start_time_from: Optional[datetime] 
    start_time_to: Optional[datetime] 
    timezone: Optional[str]  
    min_active_selections: int = None

class SearchModel(BaseModel):
    sport: Optional[SearchFilter]
    event: Optional[SearchFilter]
    selection: Optional[SearchFilter]
