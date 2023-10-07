from datetime import datetime
import pytest
import asyncpg
from pytest_mock import mocker
from repositories.sport_repository import SportRepository
from schemas import SportBase

# Create a mock for the database pool
@pytest.fixture
def db_pool_mock(mocker):
    return mocker.patch('asyncpg.pool.Pool', autospec=True)

@pytest.fixture
def sport_repository(db_pool_mock, mocker):
    return_value = [{'id': 1, 'name': 'Sport 1' , 'slug': 'sport-1', 'acitve': True}]

    mocker.patch.object(SportRepository, 'get_all', return_value=return_value)
    return SportRepository(db_pool_mock)


@pytest.fixture
def sport_repository_create(db_pool_mock, mocker):
    return_value = {'id': 1, 'name': 'Sport 1', 'slug': 'sport-1', 'active': True}
    mocker.patch.object(SportRepository, 'create', return_value=return_value)
    return SportRepository(db_pool_mock)


@pytest.fixture
def sport_repository_update(db_pool_mock, mocker):
    return_value = {'id': 1, 'name': 'Updated Sport', 'slug': 'updated-sport', 'active': False}
    mocker.patch.object(SportRepository, 'update', return_value=return_value)
    return SportRepository(db_pool_mock)


# Test case for getting all sports
@pytest.mark.asyncio
async def test_get_all_sports(sport_repository, mocker):
    # Mock the behavior of the database connection and fetch method
    mocked_connection = mocker.Mock()
    mocked_connection.fetch.return_value = [{'id': 1, 'name': 'Sport 1' , 'slug': 'sport-1', 'acitve': True}]
    mocker.patch.object(sport_repository.db_pool, 'acquire', return_value=mocked_connection)
    
    sports = await sport_repository.get_all()
    
    # Assert that the function returns the expected list of sports
    assert sports == [{'id': 1, 'name': 'Sport 1' , 'slug': 'sport-1', 'acitve': True}]


# Test case for creating a sport
@pytest.mark.asyncio
async def test_create_sport(sport_repository_create, mocker):
    # Mock the behavior of the database connection and fetchrow method
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {'id': 1, 'name': 'Sport 1'}
    
    mocker.patch.object(sport_repository_create.db_pool, 'acquire', return_value=mocked_connection)
    
    sport_data = {'id': 1, 'name': 'Sport 1' , 'slug': 'sport-1', 'acitve': True} 
    
    created_sport = await sport_repository_create.create(sport_data)
    
    assert created_sport == {'id': 1, 'name': 'Sport 1', 'slug': 'sport-1', 'active': True}


@pytest.mark.asyncio
async def test_update_sport(sport_repository_update, mocker):
    # Mock o comportamento da conexão com o banco de dados e o método update
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {'id': 1, 'name': 'Sport 1', 'slug': 'sport-1', 'active': True}
    
    mocker.patch.object(sport_repository_update.db_pool, 'acquire', return_value=mocked_connection)
    
    sport_data = {'id': 1, 'name': 'Updated Sport', 'slug': 'updated-sport', 'active': False}
    
    updated_sport = await sport_repository_update.update(sport_data)
    
    assert updated_sport == {'id': 1, 'name': 'Updated Sport', 'slug': 'updated-sport', 'active': False}

