import pytest
import asyncpg

from pytest_mock import mocker

from repositories.event_repository import EventRepository 

@pytest.fixture
def db_pool_mock(mocker):
    return mocker.patch('asyncpg.pool.Pool', autospec=True)

@pytest.fixture
def event_repository(db_pool_mock, mocker):
    mocker.patch.object(EventRepository, 'get_all', return_value=[{'id': 1, 'name': 'Event 1'}, {'id': 2, 'name': 'Event 2'}])
    return EventRepository(db_pool_mock)

@pytest.fixture
def event_repository_empty(db_pool_mock, mocker):
    mocker.patch.object(EventRepository, 'get_all', return_value=[])
    return EventRepository(db_pool_mock)


@pytest.mark.asyncio
async def test_get_all(event_repository):
    events = await event_repository.get_all()
    assert events == [{'id': 1, 'name': 'Event 1'}, {'id': 2, 'name': 'Event 2'}]

@pytest.mark.asyncio
async def test_get_all_with_events(event_repository, mocker):
    # Mock the behavior of the database connection and fetch method
    mocked_connection = mocker.Mock()
    mocked_connection.fetch.return_value = [{'id': 1, 'name': 'Event 1'}, {'id': 2, 'name': 'Event 2'}]
    mocker.patch.object(event_repository.db_pool, 'acquire', return_value=mocked_connection)
    
    events = await event_repository.get_all()
    
    # Assert that the function returns the expected list of events
    assert events == [{'id': 1, 'name': 'Event 1'}, {'id': 2, 'name': 'Event 2'}]

# Test case for get_all when the database connection fails
@pytest.mark.asyncio
async def test_get_all_db_connection_failure(event_repository_empty, mocker):
    # Mock the behavior of the database connection to simulate a failure
    mocker.patch.object(event_repository_empty.db_pool, 'acquire', side_effect=asyncpg.PostgresError("Database connection error"))
    
    events = await event_repository_empty.get_all()
    
    # Assert that the function returns an empty list when there's a database connection error
    assert events == []

@pytest.mark.asyncio
async def test_get_all_query_canceled(event_repository_empty, mocker):
    # Mock the behavior of the database connection to simulate a query canceled error
    mocker.patch.object(event_repository_empty.db_pool, 'acquire', side_effect=asyncpg.QueryCanceledError("Query canceled"))
    
    events = await event_repository_empty.get_all()
    
    # Assert that the function returns an empty list when a query is canceled
    assert events == []

# Test case for unexpected error
@pytest.mark.asyncio
async def test_get_all_unexpected_error(event_repository_empty, mocker):
    # Mock the behavior of the database connection to simulate an unexpected error
    mocker.patch.object(event_repository_empty.db_pool, 'acquire', side_effect=Exception("Unexpected error"))
    
    events = await event_repository_empty.get_all()
    
    # Assert that the function returns an empty list when an unexpected error occurs
    assert events == []
