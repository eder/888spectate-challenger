import asyncpg
import pytest
from pytest_mock import mocker
from repositories.selection_repository import SelectionRepository
from schemas import SelectionBase, SelectionOutcome


@pytest.fixture
def db_pool_mock(mocker):
    return mocker.patch("asyncpg.pool.Pool", autospec=True)


@pytest.fixture
def selection_repository(db_pool_mock, mocker):
    mocker.patch.object(
        SelectionRepository,
        "get_all",
        return_value=[
            {
                "id": 1,
                "name": "Selection 1",
                "event_id": 1,
                "price": 10.0,
                "active": True,
                "outcome": SelectionOutcome.WIN,
            }
        ],
    )
    return SelectionRepository(db_pool_mock)


@pytest.fixture
def selection_repository_empty(db_pool_mock, mocker):
    mocker.patch.object(SelectionRepository, "get_all", return_value=[])
    return SelectionRepository(db_pool_mock)


@pytest.fixture
def selection_repository_create(db_pool_mock, mocker):
    return_value = {
        "id": 1,
        "name": "Selection 1",
        "event_id": 1,
        "price": 10.0,
        "active": True,
        "outcome": SelectionOutcome.WIN,
    }

    mocker.patch.object(SelectionRepository, "create", return_value=return_value)
    return SelectionRepository(db_pool_mock)


@pytest.fixture
def selection_repository_update(db_pool_mock, mocker):
    mocker.patch.object(
        SelectionRepository,
        "update",
        return_value={
            "id": 1,
            "name": "Updated Selection",
            "event_id": 1,
            "price": 20.0,
            "active": False,
            "outcome": SelectionOutcome.LOSE,
        },
    )
    return SelectionRepository(db_pool_mock)


@pytest.mark.asyncio
async def test_get_all_selections(selection_repository, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetch.return_value = [
        {
            "id": 1,
            "name": "Selection 1",
            "event_id": 1,
            "price": 10.0,
            "active": True,
            "outcome": SelectionOutcome.WIN,
        }
    ]
    mocker.patch.object(
        selection_repository.db_pool, "acquire", return_value=mocked_connection
    )

    selections = await selection_repository.get_all()

    assert selections == [
        {
            "id": 1,
            "name": "Selection 1",
            "event_id": 1,
            "price": 10.0,
            "active": True,
            "outcome": SelectionOutcome.WIN,
        }
    ]


@pytest.mark.asyncio
async def test_create_selection(selection_repository_create, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {
        "id": 1,
        "name": "Selection 1",
        "event_id": 1,
        "price": 10.0,
        "active": True,
        "outcome": SelectionOutcome.WIN,
    }

    mocker.patch.object(
        selection_repository_create.db_pool, "acquire", return_value=mocked_connection
    )

    selection_data = {
        "name": "Selection 1",
        "event_id": 1,
        "price": 10.0,
        "active": True,
        "outcome": SelectionOutcome.WIN,
    }

    created_selection = await selection_repository_create.create(selection_data)

    assert created_selection == {
        "id": 1,
        "name": "Selection 1",
        "event_id": 1,
        "price": 10.0,
        "active": True,
        "outcome": SelectionOutcome.WIN,
    }


@pytest.mark.asyncio
async def test_update_selection(selection_repository_update, mocker):
    mocked_connection = mocker.Mock()
    mocked_connection.fetchrow.return_value = {
        "id": 1,
        "name": "Updated Selection",
        "event_id": 1,
        "price": 20.0,
        "active": False,
        "outcome": SelectionOutcome.LOSE,
    }

    mocker.patch.object(
        selection_repository_update.db_pool, "acquire", return_value=mocked_connection
    )

    selection_id = 1

    updated_selection_data = {
        "name": "Updated Selection",
        "event_id": 1,
        "price": 20.0,
        "active": False,
        "outcome": SelectionOutcome.LOSE,
    }

    updated_selection = await selection_repository_update.update(
        selection_id, updated_selection_data
    )

    assert updated_selection == {
        "id": 1,
        "name": "Updated Selection",
        "event_id": 1,
        "price": 20.0,
        "active": False,
        "outcome": SelectionOutcome.LOSE,
    }
