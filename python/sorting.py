from typing import List, Tuple, Optional
import random

def bubble_sort_(ls: List) -> List:
    nElem = len(ls)
    if nElem <= 1:
        return ls
    swap_flag = True
    while swap_flag:
        swap_flag = False
        for idx in range(nElem-1):
            if ls[idx] > ls[idx + 1]:
                ls[idx], ls[idx + 1] = ls[idx + 1], ls[idx]
                swap_flag = True
    return ls

def selection_sort_(ls: List) -> List:
    nElem = len(ls)
    if nElem <= 1:
        return ls
    for idx in range(nElem-1):
        unsortedpart = ls[idx:]
        min_val_so_far = float('inf')
        min_index_so_far = None
        for unsort_idx, unsort_elem in enumerate(unsortedpart):
            if unsort_elem < min_val_so_far:
                min_val_so_far = unsort_elem
                min_index_so_far = unsort_idx
        ls[idx], ls[idx + min_index_so_far] = ls[idx + min_index_so_far], ls[idx]
    return ls

def merge_sort(ls: List) -> List:
    nElem = len(ls)
    if nElem <= 1:
        return ls
    first_list = merge_sort(ls[:nElem // 2])
    second_list = merge_sort(ls[nElem // 2:])
    new_list = []
    while (len(first_list) != 0) and (len(second_list) != 0):
        if first_list[-1] > second_list[-1]:
            new_list.append(first_list.pop())
        else:
            new_list.append(second_list.pop())
    new_list.reverse()
    return first_list + second_list + new_list

def quicksort_(ls: List, partition_idxs: Optional[Tuple[int, int]] = None, scheme = 'hoare') -> Optional[List]:
    if partition_idxs is None:
        start = 0
        end = len(ls) - 1
    else:
        start = partition_idxs[0]
        end = partition_idxs[1]
    if start >= end:
        return
    if scheme == 'hoare':
        left_boundary, right_boundary = _hoare_partition_(ls, start, end)
    elif scheme == 'lomuto':
        left_boundary, right_boundary = _lomuto_partition_(ls, start, end)
    else:
        print('Unknown Scheme')
        return ls
    quicksort_(ls, (start, left_boundary), scheme = scheme)
    quicksort_(ls, (right_boundary, end), scheme = scheme)
    if partition_idxs is None:
        return ls
    else:
         return

def _hoare_partition_(ls: List, start: int, end: int) -> Tuple[int, int]:
    pivot = ls[random.randint(start, end)]
    left_pointer = start
    right_pointer = end
    while True:
        while ls[left_pointer] < pivot:
            left_pointer += 1
        while ls[right_pointer] > pivot:
            right_pointer -= 1
        if left_pointer >= right_pointer:
            break
        ls[right_pointer], ls[left_pointer] = ls[left_pointer], ls[right_pointer]
        left_pointer += 1
        right_pointer -= 1
    return right_pointer, right_pointer + 1

def _lomuto_partition_(ls: List, start: int, end: int) -> Tuple[int, int]:
    new_pivot_idx = start
    pivot = ls[end]
    for idx in range(start, end):
        if ls[idx] < pivot:
            ls[idx], ls[new_pivot_idx] = ls[new_pivot_idx], ls[idx]
            new_pivot_idx += 1
    ls[new_pivot_idx], ls[end] = ls[end], ls[new_pivot_idx]
    return new_pivot_idx - 1, new_pivot_idx + 1