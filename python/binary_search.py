from typing import List, Optional, Tuple, TypeVar
import random
from . import testing
from .testing import generate_random_list

T = TypeVar('T')

# Assume ls is sorted
def binary_search(ls: List[T], item: T, partition_idxs: Optional[Tuple[int, int]] = None) -> Optional[int]:
    if len(ls) == 0:
        return None
    if partition_idxs is None:
        start = 0
        end = len(ls) - 1
    else:
        start = partition_idxs[0]
        end = partition_idxs[1]
    if start > end:
        return None
    midpoint = start + (end - start) // 2
    if ls[midpoint] == item:
        return midpoint
    elif ls[midpoint] > item:
        return binary_search(ls, item, (start, midpoint - 1))
    else: # ls[midpoint] < item
        return binary_search(ls, item, (midpoint + 1, end))

def test_binary_search():
    ls = sorted(generate_random_list())
    item = random.choice(ls)
    print('Testing with included item...')
    found_index = binary_search(ls, item)
    assert ls[found_index] == item
    print(f"Item {item} found at index {found_index} ({ls[found_index]})")
    print('Testing with excluded items...')
    found_index = binary_search(ls, max(ls) + random.randint(1, 99))
    assert found_index == None
    found_index = binary_search(ls, min(ls) - random.randint(1, 99))
    assert found_index == None
    item = random.choice(list(set(range(testing.MIN_VAL, testing.MAX_VAL)) - set(ls)))
    found_index = binary_search(ls, item)
    assert found_index == None
    print('Passed!!!')