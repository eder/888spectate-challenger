from pydantic import BaseModel
from datetime import datetime

class SportBase(BaseModel):
    name: str
    slug: str
    active: bool = True

class SportCreate(SportBase):
    pass

class SportResponse(SportBase):
    id: int
