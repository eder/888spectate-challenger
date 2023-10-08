import logging

from fastapi import Depends

from db.database import get_db_pool

from repositories.event_repository import EventRepository
from services.event_service import EventService

from repositories.sport_repository import SportRepository
from services.sport_service import SportService

from repositories.selection_repository import SelectionRepository
from services.selection_service import SelectionService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_logger() -> logging.Logger:
    return logger


# Events


def get_event_repository(
    logger: logging.Logger = Depends(get_logger),
) -> EventRepository:
    """
    Dependency factory function to get an instance of EventRepository.

    Returns:
        EventRepository: An instance of EventRepository.
    """
    return EventRepository(get_db_pool(), logger)


def get_event_service(
    event_repository: EventRepository = Depends(get_event_repository),
    logger: logging.Logger = Depends(get_logger),  # Adicione esta dependência
) -> EventService:
    return EventService(event_repository, logger)


# Sports
def get_sport_repository(
    Logger: logging.Logger = Depends(get_logger),
) -> SportRepository:
    """
    Dependency factory function to get an instance of SportRepository.

    Returns:
        SportRepository: An instance of SportRepository.
    """
    return SportRepository(get_db_pool(), logger)


def get_sport_service(
    sport_repository: SportRepository = Depends(get_sport_repository),
    event_repository: EventRepository = Depends(get_event_repository),
    logger: logging.Logger = Depends(get_logger),
) -> SportService:
    """
    Dependency factory function to get an instance of SportService.

    Args:
        repo (SportRepository): An instance of SportRepository.

    Returns:
        SportService: An instance of SportService.
    """
    return SportService(
        sport_repository=sport_repository,
        event_repository=event_repository,
        logger=logger,
    )


# Selections
def get_selection_repository(
    Logger: logging.Logger = Depends(get_logger),
) -> SelectionRepository:
    """
    Dependency factory function to get an instance of SelectionRepository.

    Returns:
        SelectionRepository: An instance of SelectionRepository.
    """
    return SelectionRepository(get_db_pool(), logger)


def get_selection_service(
    selection_repository: SelectionRepository = Depends(get_selection_repository),
    event_repository: EventRepository = Depends(get_event_repository),
    logger: logging.Logger = Depends(get_logger),
) -> SelectionService:
    """
    Dependency factory function to get an instance of SelectionService.

    Args:
        repo (SelectionRepository): An instance of SelectionRepository.

    Returns:
        SelectionService: An instance of SelectionService.
    """
    return SelectionService(
        selection_repository=selection_repository,
        event_repository=event_repository,
        logger=logger,
    )
