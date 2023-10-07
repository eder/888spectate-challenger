import pytest
from utils.prepare_data_for_insert import prepare_data_for_insert 

def test_prepare_data_for_insert():
    data = {
        "name": "John",
        "age": None,
        "city": "New York",
        "country": None
    }
    result = prepare_data_for_insert(data)
    expected_result = {
        "name": "John",
        "city": "New York"
    }
    assert result == expected_result

    data = {
        "name": "Alice",
        "age": 30,
        "city": "Los Angeles",
        "country": "USA"
    }
    result = prepare_data_for_insert(data)
    expected_result = {
        "name": "Alice",
        "age": 30,
        "city": "Los Angeles",
        "country": "USA"
    }
    assert result == expected_result

    data = {}
    result = prepare_data_for_insert(data)
    expected_result = {}
    assert result == expected_result

    data = {
        "name": None,
        "age": None,
        "city": None
    }
    result = prepare_data_for_insert(data)
    expected_result = {}
    assert result == expected_result

