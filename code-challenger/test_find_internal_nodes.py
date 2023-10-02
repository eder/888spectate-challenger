import pytest
from find_internal_nodes import find_internal_nodes_num

class TestClass:
    def test_validate_non_empty_list_input(self):
        # Check if input is a list
        my_tree = [4, 4, 1, 5, -1, 4, 5]
        assert isinstance(my_tree, list), "Input should be a list"

        # Check if list is not empty
        assert len(my_tree) > 0, "Input list should not be empty"
        
        # Now you can also check the functionality if you want
        assert find_internal_nodes_num(my_tree) == 3

    def test_find_internal_nodes_1(self):
        my_tree = [4, 4, 1, 5, -1, 4, 5]
        assert find_internal_nodes_num(my_tree) == 3

    def test_find_internal_nodes_2(self):
        # A tree with no parent nodes (all values are -1)
        my_tree = [-1, -1, -1, -1]
        assert find_internal_nodes_num(my_tree) == 0


