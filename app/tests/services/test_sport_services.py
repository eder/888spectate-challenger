import logging

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
from services.sport_service import SportService
from repositories.sport_repository import SportRepository
from repositories.event_repository import EventRepository


@pytest.fixture
def mock_logger():
    return Mock(spec=logging.Logger)


@pytest.fixture
def mock_sport_repository():
    return Mock(
        spec=SportRepository,
        get_all=AsyncMock(),
        create=AsyncMock(),
        update=AsyncMock(),
    )


@pytest.fixture
def mock_event_repository():
    return Mock(spec=EventRepository, get_active_events_count=AsyncMock())


@pytest.fixture
def sport_service(mock_sport_repository, mock_event_repository, mock_logger):
    return SportService(mock_sport_repository, mock_event_repository, mock_logger)


@pytest.mark.asyncio
async def test_get_all(sport_service, mock_sport_repository):
    mock_sport_repository.get_all.return_value = [
        {"name": "Football", "slug": "football", "active": True}
    ]
    sports = await sport_service.get_all()
    assert len(sports) == 1
    assert sports[0]["name"] == "Football"


@pytest.mark.asyncio
async def test_create(sport_service, mock_sport_repository):
    sport_data = {"name": "Football", "active": True}
    mock_sport_repository.create.return_value = {
        "id": 1,
        **sport_data,
        "slug": "football",
    }
    result = await sport_service.create(sport_data)
    assert result["id"] == 1
    assert result["name"] == "Football"
    assert result["slug"] == "football"


@pytest.mark.asyncio
async def test_update_inactive_sport(
    sport_service, mock_sport_repository, mock_event_repository
):
    sport_id = 1
    sport_data = {"name": "Football Updated", "active": False}
    mock_event_repository.get_active_events_count.return_value = 0
    mock_sport_repository.update.return_value = sport_data
    updated_sport = await sport_service.update(sport_id, sport_data)
    mock_event_repository.get_active_events_count.assert_called_once_with(sport_id)
    assert updated_sport["name"] == "Football Updated"
