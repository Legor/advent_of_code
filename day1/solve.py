from pathlib import Path
from itertools import combinations
from utils import prod


def solve(input_file, combination_size):
    """Solve first or second part of the puzzle"""
    raw_input = [int(x) for x in Path('./input.txt').read_text().splitlines()]
    for c in combinations(raw_input, combination_size):
        if sum(c) == 2020:
            return prod(c)


if __name__ == "__main__":

    input_file = 'input.txt'
    print(f"Solution to first puzzle: {solve(input_file, 2)}")
    print(f"Solution to second  puzzle: {solve(input_file, 3)}")