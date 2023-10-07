from typing import List


def find_internal_nodes_num(tree: List[int]) -> int:
    """
    Function to find the number of internal nodes in a tree representation.
    The tree is represented as a list of integers where each value is an index pointing to its parent.
    The root node (or nodes without a parent) are represented by a value of -1.
    Args:
    - tree (List[int]): A list representing the tree structure.
    Returns:
    - int: The number of internal nodes (unique parents) in the tree.
    """

    # Initialize an empty dictionary to store node counts
    count = {}

    # Iterate through each node in the tree
    for node in tree:
        # Check if the current node is not a root (or a node without a parent)
        if node != -1:
            # If the node is already in the count dictionary, increment its count
            if node in count:
                count[node] += 1
            # Otherwise, add the node to the dictionary with a count of 1
            else:
                count[node] = 1

    # Return the number of unique parent nodes (internal nodes) in the tree
    return len(count)
