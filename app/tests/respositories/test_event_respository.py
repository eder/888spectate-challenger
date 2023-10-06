import pytest
from pytest_mock import mocker

from repositories.event_repository import EventRepository  # Ajuste o import para apontar para a localização real da sua classe.

@pytest.fixture
def db_pool_mock(mocker):
    return mocker.patch('asyncpg.pool.Pool', autospec=True)

@pytest.fixture
def event_repository(db_pool_mock, mocker):
    mocker.patch.object(EventRepository, 'get_all', return_value=[{'id': 1, 'name': 'Event 1'}, {'id': 2, 'name': 'Event 2'}])
    return EventRepository(db_pool_mock)

@pytest.mark.asyncio
async def test_get_all(event_repository):
    events = await event_repository.get_all()
    assert events == [{'id': 1, 'name': 'Event 1'}, {'id': 2, 'name': 'Event 2'}]

