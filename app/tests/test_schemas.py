import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas import (EventType, EventStatus, SportBase, EventBase, 
                     SelectionOutcome, 
                     SelectionBase, SearchModel, SearchFilter)

def test_event_type_enum():
    assert EventType.PREPLAY.value == "preplay"
    assert EventType.INPLAY.value == "inplay"

    with pytest.raises(ValueError):
        invalid_type = EventType("invalid_type")

def test_event_status_enum():
    assert EventStatus.STARTED.value == "started"
    assert EventStatus.PENDING.value == "pending"
    assert EventStatus.ENDED.value == "ended"
    assert EventStatus.CANCELLED.value == "cancelled"

    with pytest.raises(ValueError):
        invalid_status = EventStatus("invalid_status")

def test_sport_base_model():
    sport = SportBase(name="Soccer", slug="soccer", active=True)

    assert sport.name == "Soccer"
    assert sport.slug == "soccer"
    assert sport.active == True

    with pytest.raises(ValidationError):
        invalid_sport = SportBase(name="Soccer", slug="soccer")

def test_event_base_model():
    scheduled_start = datetime.now()
    actual_start = datetime.now()
    event = EventBase(name="Match 1", slug="match-1", active=True, type=EventType.PREPLAY,
                      status=EventStatus.STARTED, sport_id=1, 
                      scheduled_start=scheduled_start, actual_start=actual_start)

    assert event.name == "Match 1"
    assert event.slug == "match-1"
    assert event.active == True
    assert event.type == EventType.PREPLAY
    assert event.status == EventStatus.STARTED
    assert event.sport_id == 1
    assert event.scheduled_start == scheduled_start
    assert event.actual_start == actual_start

    with pytest.raises(ValidationError):
        invalid_event = EventBase(name="Match 1", slug="match-1", active=True, 
                                  type="invalid_type", status=EventStatus.STARTED, 
                                  sport_id=1, scheduled_start=scheduled_start, 
                                  actual_start=actual_start)

def test_selection_base_model():
    selection = SelectionBase(name="Team A", event_id=1, price=1.5, active=True, 
                              outcome=SelectionOutcome.UNSETTLED)

    assert selection.name == "Team A"
    assert selection.event_id == 1
    assert selection.price == 1.5
    assert selection.active == True
    assert selection.outcome == SelectionOutcome.UNSETTLED

    with pytest.raises(ValidationError):
        invalid_selection = SelectionBase(name="Team A", event_id=1, price="invalid_price", 
                                          active=True, outcome=SelectionOutcome.UNSETTLED)


def test_valid_search_model():
    data = {
        "sport": {
            "name_regex": "^[A-Z]",
            "min_active_count": 5,
            "start_time_from": "2023-10-04T00:00:00",
            "start_time_to": "2023-10-10T23:59:59",
            "timezone": "UTC"
        },
        "event": {
            "name_regex": "^[A-Z]",
            "min_active_count": 5,
            "start_time_from": "2023-10-04T00:00:00",
            "start_time_to": "2023-10-10T23:59:59",
            "timezone": "UTC"
        }
    }

    search_model = SearchModel(**data)
    assert isinstance(search_model.sport, SearchFilter)
    assert search_model.sport.name_regex == "^[A-Z]"
    assert search_model.sport.min_active_count == 5
    assert search_model.sport.start_time_from == datetime(2023, 10, 4, 0, 0, 0)
    assert search_model.sport.start_time_to == datetime(2023, 10, 10, 23, 59, 59)
    assert search_model.sport.timezone == "UTC"

def test_invalid_min_active_count():
    data = {
        "sport": {
            "min_active_count": -5
        }
    }

    try:
        search_model = SearchModel(**data)
    except ValidationError as e:
        assert len(e.errors()) == 1
        assert e.errors()[0]["loc"] == ("sport", "min_active_count")
        assert "ensure this value is greater than or equal to 0" in e.errors()[0]["msg"]

def test_missing_required_fields():
    data = {}

    try:
        search_model = SearchModel(**data)
    except ValidationError as e:
        assert len(e.errors()) == 0  
