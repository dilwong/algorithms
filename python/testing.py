import random

MAX_LEN = 9999
MIN_VAL = -9999
MAX_VAL = 9999

def generate_random_list(length = None, minimum = MIN_VAL, maximum = MAX_VAL):
    if length is None:
        length = random.randint(0, MAX_LEN)
    ls = [random.randint(minimum, maximum) for _ in range(length)]
    return ls

def test_sort(sort_function):
    ls = generate_random_list()
    sortedls = sort_function(ls)
    return sortedls == sorted(sortedls)