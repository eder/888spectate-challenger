from pydantic import BaseModel
from datetime import datetime

class SportBase(BaseModel):
    name: str
    slug: str
    active: bool

class EventBase(BaseModel):
    name: str
    slug: str
    active: bool
    type: str
    sport: SportBase
    status: str
    scheduled_start: datetime
    actual_start: datetime

class SelectionBase(BaseModel):
    name: str
    event: EventBase
    price: float
    active: bool
    outcome: str

