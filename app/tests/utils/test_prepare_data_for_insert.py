import pytest
from utils.prepare_data_for_insert import prepare_data_for_insert 

def test_prepare_data_with_values():
    data = {
        "field1": "value1",
        "field2": "value2",
        "field3": "value3"
    }
    result = prepare_data_for_insert(data)
    
    assert result["original_data"] == data
    assert result["set_clause"] == "field1=$1, field2=$2, field3=$3"
    assert result["values"] == ["value1", "value2", "value3"]

def test_prepare_data_with_none_values():
    data = {
        "field1": "value1",
        "field2": None,
        "field3": "value3"
    }
    result = prepare_data_for_insert(data)
    
    assert result["original_data"] == data
    assert result["set_clause"] == "field1=$1, field3=$2"
    assert result["values"] == ["value1", "value3"]

def test_prepare_data_with_empty_dict():
    data = {}
    result = prepare_data_for_insert(data)
    
    assert result["original_data"] == data
    assert result["set_clause"] == ""
    assert result["values"] == []

if __name__ == "__main__":
    pytest.main()

