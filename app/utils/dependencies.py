from fastapi import Depends

from repositories.event_repository import EventRepository
from services.event_service import EventService

from repositories.sport_repository import SportRepository
from services.sport_service import SportService

from repositories.selection_repository import SelectionRepository
from services.selection_service import SelectionService



from db.database import get_db_pool

def get_event_repository() -> EventRepository:
    return EventRepository(get_db_pool())

def get_event_service(repo: EventRepository = Depends(get_event_repository)) -> EventService:
    return EventService(repository=repo)


def get_sport_repository() -> SportRepository:
    return SportRepository(get_db_pool())

def get_sport_service(repo: SportRepository = Depends(get_sport_repository)) -> SportService:
    return SportService(repository=repo)

def get_selection_repository() -> SelectionRepository:
    return SelectionRepository(get_db_pool())

def get_selection_service(repo: SelectionRepository = Depends(get_selection_repository)) -> SelectionService:
    return SelectionService(repository=repo)
