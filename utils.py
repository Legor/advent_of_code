from pathlib import Path

def input(file='input.txt'):
    return [int(x) for x in Path(file).read_text().splitlines()]

def prod(numbers):
    y = 1
    for x in numbers:
        y *= x
    return y