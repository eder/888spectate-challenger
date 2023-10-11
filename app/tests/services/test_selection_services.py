import logging

import pytest
from unittest.mock import Mock, patch
from services.selection_service import SelectionService
from repositories.selection_repository import SelectionRepository
from repositories.event_repository import EventRepository
from schemas import SelectionOutcome


@pytest.fixture
def mocked_selection_repository():
    return Mock(spec=SelectionRepository)


@pytest.fixture
def mocked_event_repository():
    return Mock(spec=EventRepository)


@pytest.fixture
def mocked_logger():
    return Mock(spec=logging.Logger)


@pytest.fixture
def selection_service(
    mocked_selection_repository, mocked_event_repository, mocked_logger
):
    return SelectionService(
        mocked_selection_repository, mocked_event_repository, mocked_logger
    )
