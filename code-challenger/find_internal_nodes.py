from typing import List

def find_internal_nodes_num(tree: List[int]) -> int:
   
    count = {}
    for node in tree:
        if node != -1:
            if node in count:
                count[node] += 1
            else:
                count[node] = 1

    return len(count)

