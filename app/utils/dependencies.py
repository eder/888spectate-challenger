from fastapi import Depends
from repositories.event_repository import EventRepository
from services.event_service import EventService
from db.database import get_db_pool

def get_event_repository() -> EventRepository:
    return EventRepository(get_db_pool())

def get_event_service(repo: EventRepository = Depends(get_event_repository)) -> EventService:
    return EventService(repository=repo)

