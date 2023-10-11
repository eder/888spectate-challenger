import pytest
import datetime
from unittest.mock import Mock, AsyncMock, patch
from schemas import EventType, EventStatus
from services.event_service import EventService
from repositories.event_repository import EventRepository
import logging


@pytest.fixture
def mock_event_repository():
    return Mock(
        spec=EventRepository,
        get_all=AsyncMock(),
        create=AsyncMock(),
        update=AsyncMock(),
        get_events_selections=AsyncMock(),
        filter_events=AsyncMock(),
    )


@pytest.fixture
def mock_logger():
    return Mock(spec=logging.Logger)


@pytest.fixture
def event_service(mock_event_repository, mock_logger):
    return EventService(mock_event_repository, mock_logger)


@pytest.mark.asyncio
async def test_get_all(event_service, mock_event_repository):
    mock_event_repository.get_all.return_value = [{"id": 1}]
    result = await event_service.get_all()
    assert result == [{"id": 1}]
    mock_event_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_create(event_service, mock_event_repository):
    mock_event = {
        "name": "TestEvent",
        "active": True,
        "type": "TestType",
        "status": "TestStatus",
        "sport_id": 1,
        "scheduled_start": datetime.datetime.now(),
        "actual_start": datetime.datetime.now(),
    }

    await event_service.create(mock_event)

    mock_event_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_update(event_service, mock_event_repository):
    mock_event = {"name": "UpdatedTestEvent"}
    event_id = 1

    await event_service.update(event_id, mock_event)

    mock_event_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_get_events_selections(event_service, mock_event_repository):
    mock_event_repository.get_events_selections.return_value = [{"id": 1}]
    result = await event_service.get_events_selections()
    assert result == [{"id": 1}]
    mock_event_repository.get_events_selections.assert_called_once()


@pytest.mark.asyncio
async def test_filter_events(event_service, mock_event_repository):
    criteria = {"name_regex": "Test", "active": True}

    mock_event_repository.filter_events.return_value = [{"id": 1, "name": "TestEvent"}]

    result = await event_service.filter_events(criteria)
    assert result == [{"id": 1, "name": "TestEvent"}]
    mock_event_repository.filter_events.assert_called_once()
