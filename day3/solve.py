from pathlib import Path
from utils import prod


def count_trees(d_x, d_y, input_file):

    # prepare data
    raw_input = Path(input_file).read_text().splitlines()
    grid = [[0 if x == '.' else 1 for x in row] for row in raw_input]
    rows, cols = len(grid), len(grid[0])

    x_i = y_i = 0
    n_trees = 0
    while True:
        x_i += d_x
        if x_i >= cols:
            x_i = x_i - cols
        y_i += d_y
        if y_i >= rows:
            break
        n_trees += grid[y_i][x_i]
    return n_trees


def solve_first(input_file):
    return count_trees(3, 1, input_file)


def solve_second(input_file):

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return prod([count_trees(s[0], s[1], input_file) for s in slopes])


if __name__ == "__main__":
    input_file = 'input.txt'
    print(f"Solution to first puzzle: {solve_first(input_file)}")
    print(f"Solution to second  puzzle: {solve_second(input_file)}")
