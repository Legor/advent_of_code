from pathlib import Path


def input(file='input.txt', convert_fn=None, split=True):
    lines = Path(file).read_text()
    if split:
        lines = lines.splitlines()
    if convert_fn:
        lines = [convert_fn(x) for x in lines]
    return lines


def l_to_i(li):
    """Map all elements of a list to int"""
    return list(map(int, li))


def chunks(xs, n):
    """split list into chunks of size n"""
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))


def bits_to_dec(arr):
    """
    [False, True, True] --> 3
    [1, 0, 1, 0] --> 6
    "0111" --> 7
    [1, '0', 0, False, '1', True] --> 35
    """
    return int("".join([str(int(x)) for x in arr]), 2)


def prod(numbers):
    y = 1
    for x in numbers:
        y *= x
    return y