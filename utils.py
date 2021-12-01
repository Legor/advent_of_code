from pathlib import Path


def input(file='input.txt', convert_fn=None):
    lines = [int(x) for x in Path(file).read_text().splitlines()]
    if convert_fn:
        lines = [convert_fn(x) for x in lines]
    return lines


def prod(numbers):
    y = 1
    for x in numbers:
        y *= x
    return y