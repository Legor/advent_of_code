# https://adventofcode.com/2024/day/19

from utils import parse_input


def count_arrangements(design, patterns):
    """Count all possible ways to arrange patterns to form the design using DP."""
    n = len(design)
    # for each sub pattern up to the i-th character in design,
    # counts the number of ways this sub pattern can be formed using the given patterns
    sub_count = [0] * (n + 1)
    # Base case: one way to form an empty prefix
    sub_count[0] = 1
    # iterate through each position in the design
    for i in range(1, n + 1):
        for pattern in patterns:
            # check each pattern if it fits into the sub pattern and matches the end
            if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                sub_count[i] += sub_count[i - len(pattern)]  # Add ways to form the remaining prefix

    return sub_count[n]

def solve(patterns, designs):
    """Solve the first aprt of the puzzle."""
    # Calculate total arrangements
    return sum([count_arrangements(design, patterns) > 0 for design in designs])

def solve2(patterns, designs):
    """Solve the second part of the puzzle."""
    return sum([count_arrangements(design, patterns) for design in designs])


if __name__ == "__main__":

    # Parse input
    patterns, designs = parse_input(split_on="\n\n")
    patterns = [p.strip() for p in patterns.split(",")]
    designs = designs.split()

    # Sort patterns by length (shortest to longest for efficiency)
    patterns = sorted(patterns, key=len)

    print(f"Solution to first puzzle: {solve(patterns, designs)}")
    print(f"Solution to second puzzle: {solve2(patterns, designs)}")
