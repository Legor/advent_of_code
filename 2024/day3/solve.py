# https://adventofcode.com/2024/day/3

from utils import parse_input
import re


def find_mul(line):
    pattern = "mul\((\d+),(\d+)\)"
    return [(m.groups(), m.start()) for m in re.finditer(pattern, line)]


def find_pos(pattern, line):
    return [m.start() for m in re.finditer(pattern, line)]


def solve(instruction):
    """Solve first part of the puzzle"""
    return sum(
        [int(numbers[0]) * int(numbers[1]) for numbers, _ in find_mul(instruction)]
    )


def solve2(instruction):
    """Solve second part of the puzzle"""

    def get_previous_i(ins_i, i):
        """Return the most recent number from ins_i before i or None if there isn't any smaller one."""
        max_i = [j for j in ins_i if j < i]
        return max(max_i) if max_i else None

    result = 0
    muls = find_mul(instruction)
    dos = find_pos("do\(\)", instruction)
    donts = find_pos("don't\(\)", instruction)
    enabled = True
    for mul, mul_i in muls:
        do_max_i = get_previous_i(dos, mul_i)
        dont_max_i = get_previous_i(donts, mul_i)

        # update calc status
        if do_max_i and dont_max_i:
            enabled = do_max_i > dont_max_i
        else:
            if do_max_i and not dont_max_i:
                enabled = True
            elif dont_max_i and not do_max_i:
                enabled = False

        if enabled:
            result += int(mul[0]) * int(mul[1])
    return result


if __name__ == "__main__":
    instruction = parse_input(split_on=None)
    print(f"Solution to first puzzle: {solve(instruction)}")
    print(f"Solution to second  puzzle: {solve2(instruction)}")
