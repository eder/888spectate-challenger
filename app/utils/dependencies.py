from fastapi import Depends

from repositories.event_repository import EventRepository
from services.event_service import EventService

from repositories.sport_repository import SportRepository
from services.sport_service import SportService

from repositories.selection_repository import SelectionRepository
from services.selection_service import SelectionService

from db.database import get_db_pool

 # Events
def get_event_repository() -> EventRepository:
    """
    Dependency factory function to get an instance of EventRepository.

    Returns:
        EventRepository: An instance of EventRepository.
    """
    return EventRepository(get_db_pool())

def get_event_service(event_repository: EventRepository = Depends(get_event_repository)) -> EventService:
    """
    Dependency factory function to get an instance of EventService.

    Args:
        event_repository (EventRepository): An instance of EventRepository.

    Returns:
        EventService: An instance of EventService.
    """
    return EventService(event_repository)

# Sports 
def get_sport_repository() -> SportRepository:
    """
    Dependency factory function to get an instance of SportRepository.

    Returns:
        SportRepository: An instance of SportRepository.
    """
    return SportRepository(get_db_pool())

def get_sport_service(repo: SportRepository = Depends(get_sport_repository)) -> SportService:
    """
    Dependency factory function to get an instance of SportService.

    Args:
        repo (SportRepository): An instance of SportRepository.

    Returns:
        SportService: An instance of SportService.
    """
    return SportService(sport_repository=repo)


# Selections
def get_selection_repository() -> SelectionRepository:
    """
    Dependency factory function to get an instance of SelectionRepository.

    Returns:
        SelectionRepository: An instance of SelectionRepository.
    """
    return SelectionRepository(get_db_pool())

def get_selection_service(repo: SelectionRepository = Depends(get_selection_repository)) -> SelectionService:
    """
    Dependency factory function to get an instance of SelectionService.

    Args:
        repo (SelectionRepository): An instance of SelectionRepository.

    Returns:
        SelectionService: An instance of SelectionService.
    """
    return SelectionService(selection_repository=repo)

