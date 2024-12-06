# small simple helper functions
import copy
import math
import re
from functools import reduce
from typing import Iterable, Union

def get_mask(arr: list[list], cond):
    """For a 2-d list return a binary array of the same shape (a mask) according to the given condition"""

    mask = copy.deepcopy(arr)
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            mask[i][j] = cond(arr[i][j])
    return mask


def l_to_i(li: list):
    """Map all elements of a list to int"""
    return list(map(int, li))


def chunks(xs: list, n: int):
    """split list into chunks of size n"""
    n = max(1, n)
    return (xs[i: i + n] for i in range(0, len(xs), n))


def bits_to_dec(arr: Iterable):
    """
    Convert a binary pattern to the decimal representation

    [False, True, True] --> 3
    [1, 0, 1, 0] --> 6
    "0111" --> 7
    [1, '0', 0, False, '1', True] --> 35
    """
    return int("".join([str(int(x)) for x in arr]), 2)


def prod(numbers: Iterable):
    """Return the product of all numbers in the given list."""
    y = 1
    for x in numbers:
        y *= x
    return y


def sign(x: Union[int, float]):
    """Return the sign of the number (-1, or 1). Will return 1 for zero."""
    return -1 if x < 0 else 1


def lcm(a: int, b: int):
    """Calculate the least common multiple (LCM) for two numbers."""
    return abs(a * b) // math.gcd(a, b)


def find_lcm(numbers: list[int]):
    """Calculate the least common multiple (LCM) for a list of numbers."""
    return reduce(lcm, numbers)


def get_nb_indices(y: int, x: int):
    """Generate a list of 2d neighborhood indices (8-connected) for a given center coordinate.
    The center coordinate itself is excluded."""
    return [
        (j, i)
        for i in range(x - 1, x + 2)
        for j in range(y - 1, y + 2)
        if (j, i) != (y, x)
    ]


def substring_idx(text: str, substring: str):
    """Return the starting indices of all occurrences of substring in text."""
    pattern = re.escape(substring)
    return [match.start() for match in re.finditer(pattern, text)]


def find_pattern_in_lines(lines: list, pattern: str):
    """Return the matches of all provided regular expressions in all given lines."""
    return [list(re.finditer(pattern, line)) for line in lines]
