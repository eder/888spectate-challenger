from fastapi import Depends

from db.database import get_db_pool

from repositories.event_repository import EventRepository
from services.event_service import EventService

from repositories.sport_repository import SportRepository
from services.sport_service import SportService

from repositories.selection_repository import SelectionRepository
from services.selection_service import SelectionService

from repositories.search_repository import SearchRepository
from services.search_service import SearchService


# Events
def get_event_repository() -> EventRepository:
    """
    Dependency factory function to get an instance of EventRepository.

    Returns:
        EventRepository: An instance of EventRepository.
    """
    return EventRepository(get_db_pool())


def get_event_service(
    event_repository: EventRepository = Depends(get_event_repository),
) -> EventService:
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


def get_sport_service(
    sport_repository: SportRepository = Depends(get_sport_repository),
    event_repository: EventRepository = Depends(get_event_repository),
) -> SportService:
    """
    Dependency factory function to get an instance of SportService.

    Args:
        repo (SportRepository): An instance of SportRepository.

    Returns:
        SportService: An instance of SportService.
    """
    return SportService(
        sport_repository=sport_repository, event_repository=event_repository
    )


# Selections
def get_selection_repository() -> SelectionRepository:
    """
    Dependency factory function to get an instance of SelectionRepository.

    Returns:
        SelectionRepository: An instance of SelectionRepository.
    """
    return SelectionRepository(get_db_pool())


def get_selection_service(
    selection_repository: SelectionRepository = Depends(get_selection_repository),
    event_repository: EventRepository = Depends(get_event_repository),
) -> SelectionService:
    """
    Dependency factory function to get an instance of SelectionService.

    Args:
        repo (SelectionRepository): An instance of SelectionRepository.

    Returns:
        SelectionService: An instance of SelectionService.
    """
    return SelectionService(
        selection_repository=selection_repository, event_repository=event_repository
    )


# Searches
def get_search_repository() -> SearchRepository:
    """
    Dependency factory function to get an instance of SearchesRepository.

    Returns:
        SearchesRepository: An instance of SearchesRepository.
    """
    return SearchRepository(get_db_pool())


def get_search_service(
    repo: SearchRepository = Depends(get_search_repository),
) -> SearchService:
    """
    Dependency factory function to get an instance of SearchesService.

    Args:
        repo (SearchesRepository): An instance of SearchesRepository.

    Returns:
        SelectionService: An instance of SelectionService.
    """
    return SearchService(search_repository=repo)
