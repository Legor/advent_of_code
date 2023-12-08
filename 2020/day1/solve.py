from itertools import combinations
from utils import prod, parse_input


def solve(combination_size):
    """Solve first or second part of the puzzle"""
    raw_input = parse_input(convert_fn=int)
    for c in combinations(raw_input, combination_size):
        if sum(c) == 2020:
            return prod(c)


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve(2)}")
    print(f"Solution to second  puzzle: {solve(3)}")