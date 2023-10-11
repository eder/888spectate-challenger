import logging
import asyncpg
import pytest
from pytest_mock import mocker
from datetime import datetime

from repositories.sport_repository import SportRepository
from schemas import SportBase


@pytest.fixture
def logger_mock(mocker):
    return mocker.Mock(spec=["info", "error", "debug", "warning"])


@pytest.fixture
def db_pool_mock(mocker):
    return mocker.patch("asyncpg.pool.Pool", autospec=True)


@pytest.fixture
def sport_repository(db_pool_mock, logger_mock, mocker):
    return_value = [{"id": 1, "name": "Sport 1", "slug": "sport-1", "acitve": True}]

    mocker.patch.object(SportRepository, "get_all", return_value=return_value)
    return SportRepository(db_pool_mock, logger_mock)


@pytest.fixture
def sport_repository_create(db_pool_mock, logger_mock, mocker):
    return_value = {"id": 1, "name": "Sport 1", "slug": "sport-1", "active": True}
    mocker.patch.object(SportRepository, "create", return_value=return_value)
    return SportRepository(db_pool_mock, logger_mock)


@pytest.fixture
def sport_repository_update(db_pool_mock, logger_mock, mocker):
    return_value = {
        "id": 1,
        "name": "Updated Sport",
        "slug": "updated-sport",
        "active": False,
    }
    mocker.patch.object(SportRepository, "update", return_value=return_value)
    return SportRepository(db_pool_mock, logger_mock)


@pytest.mark.asyncio
async def test_get_all_sports(sport_repository, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetch.return_value = [
        {"id": 1, "name": "Sport 1", "slug": "sport-1", "acitve": True}
    ]
    mocker.patch.object(
        sport_repository.db_pool, "acquire", return_value=mocked_connection
    )

    sports = await sport_repository.get_all()

    assert sports == [{"id": 1, "name": "Sport 1", "slug": "sport-1", "acitve": True}]


@pytest.mark.asyncio
async def test_create_sport(sport_repository_create, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {"id": 1, "name": "Sport 1"}

    mocker.patch.object(
        sport_repository_create.db_pool, "acquire", return_value=mocked_connection
    )

    sport_data = {"id": 1, "name": "Sport 1", "slug": "sport-1", "acitve": True}

    created_sport = await sport_repository_create.create(sport_data)

    assert created_sport == {
        "id": 1,
        "name": "Sport 1",
        "slug": "sport-1",
        "active": True,
    }


@pytest.mark.asyncio
async def test_update_sport(sport_repository_update, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {
        "id": 1,
        "name": "Sport 1",
        "slug": "sport-1",
        "active": True,
    }

    mocker.patch.object(
        sport_repository_update.db_pool, "acquire", return_value=mocked_connection
    )

    sport_data = {
        "id": 1,
        "name": "Updated Sport",
        "slug": "updated-sport",
        "active": False,
    }

    updated_sport = await sport_repository_update.update(sport_data)

    assert updated_sport == {
        "id": 1,
        "name": "Updated Sport",
        "slug": "updated-sport",
        "active": False,
    }
