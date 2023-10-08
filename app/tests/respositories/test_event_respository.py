from datetime import datetime
import asyncpg
import pytest
from repositories.event_repository import EventRepository
from schemas import EventType, EventStatus, SearchFilter
import logging


@pytest.fixture
def logger_mock(mocker):
    return mocker.Mock(spec=["info", "error", "debug", "warning"])


@pytest.fixture
def db_pool_mock(mocker):
    return mocker.patch("asyncpg.pool.Pool", autospec=True)


@pytest.fixture
def event_repository(db_pool_mock, logger_mock, mocker):
    mocker.patch.object(
        EventRepository,
        "get_all",
        return_value=[{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}],
    )
    return EventRepository(db_pool_mock, logger_mock)


@pytest.fixture
def event_repository_empty(db_pool_mock, logger_mock, mocker):
    mocker.patch.object(EventRepository, "get_all", return_value=[])
    return EventRepository(db_pool_mock, logger_mock)


@pytest.fixture
def event_repository_create(db_pool_mock, logger_mock, mocker):
    return_value = {
        "id": 1,
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": "concert",
        "sport_id": 2,
        "status": "scheduled",
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }
    mocker.patch.object(EventRepository, "create", return_value=return_value)
    return EventRepository(db_pool_mock, logger_mock)


@pytest.fixture
def event_repository_update(db_pool_mock, logger_mock, mocker):
    return_value = {
        "id": 1,
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": "conference",
        "sport_id": 2,
        "status": "completed",
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }
    mocker.patch.object(EventRepository, "update", return_value=return_value)
    return EventRepository(db_pool_mock, logger_mock)


@pytest.mark.asyncio
async def test_get_all(event_repository):
    events = await event_repository.get_all()
    assert events == [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]


@pytest.mark.asyncio
async def test_get_all_with_events(event_repository, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetch.return_value = [
        {"id": 1, "name": "Event 1"},
        {"id": 2, "name": "Event 2"},
    ]
    mocker.patch.object(
        event_repository.db_pool, "acquire", return_value=mocked_connection
    )
    events = await event_repository.get_all()
    assert events == [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]


@pytest.mark.asyncio
async def test_get_all_db_connection_failure(event_repository_empty, mocker):
    mocker.patch.object(
        event_repository_empty.db_pool,
        "acquire",
        side_effect=asyncpg.PostgresError("Database connection error"),
    )
    events = await event_repository_empty.get_all()
    assert events == []


@pytest.mark.asyncio
async def test_get_all_query_canceled(event_repository_empty, mocker):
    mocker.patch.object(
        event_repository_empty.db_pool,
        "acquire",
        side_effect=asyncpg.QueryCanceledError("Query canceled"),
    )
    events = await event_repository_empty.get_all()
    assert events == []


@pytest.mark.asyncio
async def test_get_all_unexpected_error(event_repository_empty, mocker):
    mocker.patch.object(
        event_repository_empty.db_pool,
        "acquire",
        side_effect=Exception("Unexpected error"),
    )
    events = await event_repository_empty.get_all()
    assert events == []


@pytest.mark.asyncio
async def test_create_valid_event(event_repository_create, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {
        "id": 1,
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": "concert",
        "sport_id": 2,
        "status": "scheduled",
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }
    mocker.patch.object(
        event_repository_create.db_pool, "acquire", return_value=mocked_connection
    )
    event_data = {
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": EventType.PREPLAY,
        "sport_id": 2,
        "status": EventStatus.PENDING,
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }
    created_event = await event_repository_create.create(event_data)
    assert created_event == {
        "id": 1,
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": "concert",
        "sport_id": 2,
        "status": "scheduled",
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }


@pytest.mark.asyncio
async def test_update_event(event_repository_update, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {
        "id": 1,
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": "conference",
        "sport_id": 2,
        "status": "completed",
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }
    mocker.patch.object(
        event_repository_update.db_pool, "acquire", return_value=mocked_connection
    )
    event_id = 1
    updated_event_data = {
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": EventType.PREPLAY,
        "sport_id": 2,
        "status": EventStatus.PENDING,
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }
    updated_event = await event_repository_update.update(event_id, updated_event_data)
    assert updated_event == {
        "id": 1,
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": "conference",
        "sport_id": 2,
        "status": "completed",
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }


# Add other tests and methods if needed.
from datetime import datetime
import asyncpg
import pytest
from repositories.event_repository import EventRepository
from schemas import EventType, EventStatus, SearchFilter


@pytest.fixture
def db_pool_mock(mocker):
    return mocker.patch("asyncpg.pool.Pool", autospec=True)


@pytest.fixture
def event_repository(db_pool_mock, mocker):
    mocker.patch.object(
        EventRepository,
        "get_all",
        return_value=[{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}],
    )
    return EventRepository(db_pool_mock)


@pytest.fixture
def event_repository_empty(db_pool_mock, mocker):
    mocker.patch.object(EventRepository, "get_all", return_value=[])
    return EventRepository(db_pool_mock)


@pytest.fixture
def event_repository_create(db_pool_mock, mocker):
    return_value = {
        "id": 1,
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": "concert",
        "sport_id": 2,
        "status": "scheduled",
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }
    mocker.patch.object(EventRepository, "create", return_value=return_value)
    return EventRepository(db_pool_mock)


@pytest.fixture
def event_repository_update(db_pool_mock, mocker):
    return_value = {
        "id": 1,
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": "conference",
        "sport_id": 2,
        "status": "completed",
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }
    mocker.patch.object(EventRepository, "update", return_value=return_value)
    return EventRepository(db_pool_mock)


@pytest.mark.asyncio
async def test_get_all(event_repository):
    events = await event_repository.get_all()
    assert events == [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]


@pytest.mark.asyncio
async def test_get_all_with_events(event_repository, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetch.return_value = [
        {"id": 1, "name": "Event 1"},
        {"id": 2, "name": "Event 2"},
    ]
    mocker.patch.object(
        event_repository.db_pool, "acquire", return_value=mocked_connection
    )
    events = await event_repository.get_all()
    assert events == [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]


@pytest.mark.asyncio
async def test_get_all_db_connection_failure(event_repository_empty, mocker):
    mocker.patch.object(
        event_repository_empty.db_pool,
        "acquire",
        side_effect=asyncpg.PostgresError("Database connection error"),
    )
    events = await event_repository_empty.get_all()
    assert events == []


@pytest.mark.asyncio
async def test_get_all_query_canceled(event_repository_empty, mocker):
    mocker.patch.object(
        event_repository_empty.db_pool,
        "acquire",
        side_effect=asyncpg.QueryCanceledError("Query canceled"),
    )
    events = await event_repository_empty.get_all()
    assert events == []


@pytest.mark.asyncio
async def test_get_all_unexpected_error(event_repository_empty, mocker):
    mocker.patch.object(
        event_repository_empty.db_pool,
        "acquire",
        side_effect=Exception("Unexpected error"),
    )
    events = await event_repository_empty.get_all()
    assert events == []


@pytest.mark.asyncio
async def test_create_valid_event(event_repository_create, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {
        "id": 1,
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": "concert",
        "sport_id": 2,
        "status": "scheduled",
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }
    mocker.patch.object(
        event_repository_create.db_pool, "acquire", return_value=mocked_connection
    )
    event_data = {
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": EventType.PREPLAY,
        "sport_id": 2,
        "status": EventStatus.PENDING,
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }
    created_event = await event_repository_create.create(event_data)
    assert created_event == {
        "id": 1,
        "name": "Event 1",
        "slug": "event-1",
        "active": True,
        "type": "concert",
        "sport_id": 2,
        "status": "scheduled",
        "scheduled_start": datetime(2023, 10, 6, 12, 0, 0),
        "actual_start": datetime(2023, 10, 6, 13, 0, 0),
    }


@pytest.mark.asyncio
async def test_update_event(event_repository_update, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {
        "id": 1,
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": "conference",
        "sport_id": 2,
        "status": "completed",
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }
    mocker.patch.object(
        event_repository_update.db_pool, "acquire", return_value=mocked_connection
    )
    event_id = 1
    updated_event_data = {
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": EventType.PREPLAY,
        "sport_id": 2,
        "status": EventStatus.PENDING,
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }
    updated_event = await event_repository_update.update(event_id, updated_event_data)
    assert updated_event == {
        "id": 1,
        "name": "Updated Event",
        "slug": "updated-event",
        "active": False,
        "type": "conference",
        "sport_id": 2,
        "status": "completed",
        "scheduled_start": datetime(2023, 10, 7, 12, 0, 0),
        "actual_start": datetime(2023, 10, 7, 13, 0, 0),
    }
