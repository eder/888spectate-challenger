import pytest
from utils.query_builder import QueryBuilder


# Fixture function to create an instance of QueryBuilder for each test
@pytest.fixture
def query_builder():
    return QueryBuilder("test_table")


# Test to verify the construction of a SELECT query
def test_build_query(query_builder):
    query = query_builder.build_query()
    assert query == "SELECT * FROM test_table"


# Test to verify the construction of an INSERT query
def test_build_insert_query(query_builder):
    insert_data = {"name": "John", "age": "30"}
    query_builder.add_insert_data(insert_data)
    query = query_builder.build_insert_query()
    assert (
        query == "INSERT INTO test_table (name, age) VALUES ('John', '30') RETURNING *"
    )


# Test to verify the construction of an UPDATE query
def test_build_update_query(query_builder):
    query_builder.add_condition("id", "1")
    update_data = {"name": "NewName", "age": "25"}
    query_builder.add_update_data(update_data)
    query = query_builder.build_update_query()
    assert (
        query
        == "UPDATE test_table SET name = 'NewName', age = '25' WHERE id = '1' RETURNING *"
    )


# Test to verify that a ValueError is raised when trying to build an UPDATE query without conditions
def test_build_update_query_without_conditions(query_builder):
    update_data = {"name": "NewName", "age": "25"}
    query_builder.add_update_data(update_data)
    with pytest.raises(ValueError):
        query_builder.build_update_query()
