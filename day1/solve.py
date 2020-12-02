from pathlib import Path
from itertools import combinations

def solve_first(input_file):
    """Solve first part of the puzzle"""
    raw_input = [int(x) for x in Path('./input.txt').read_text().splitlines()]
    for c in combinations(raw_input, 2):
        if c[0] + c[1] == 2020:
            return c[0] * c[1]


def solve_second(input_file):
    """Solve first part of the puzzle"""
    raw_input = [int(x) for x in Path('./input.txt').read_text().splitlines()]
    for c in combinations(raw_input, 3):
        if c[0] + c[1] + c[2] == 2020:
            return c[0] * c[1] * c[2]

if __name__ == "__main__":

    input_file = 'input.txt'
    print(f"Solution of first puzzle: {solve_first(input_file)}")
    print(f"Solution of second  puzzle: {solve_second(input_file)}")