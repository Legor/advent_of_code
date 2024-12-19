# https://adventofcode.com/2024/day/18

from utils import Grid, Graph, parse_input
from utils.algorithms import shortest_path


def get_path(grid: Grid, byte_list: list[tuple[int, int]]):
    """After adding a list of bytes, check if there is a path from top-left to bottom-right.

    Returns the path if there is one, otherwise None."""
    grid.set_value(byte_list, '#')
    # Initialize the graph, allow only vertical and horizontal movement if its not a '#'
    graph = Graph.from_grid(grid, nb_mask=Grid.cross(3), decision_fn=lambda x, y: y != ['#'])
    path = shortest_path(graph, start=(0, 0), end=(grid.height-1, grid.width-1))
    grid.set_value(byte_list, '.')  # Reset grid to previous state
    return path


def solve(grid, bytes):
    """Solve first part of the puzzle."""
    return len(get_path(grid, bytes[:1024]))


def solve2(grid, bytes):
    """Solve second part of the puzzle."""

    # we know that the first 1024 bytes work already
    grid.set_value(bytes[:1024], '#')
    remaining_bytes = bytes[1024:]

    # Binary search for the blocking byte
    left, right = 0, len(remaining_bytes) - 1
    while left <= right:
        mid = (left + right) // 2

        # Check if adding the first `mid+1` bytes blocks the path
        if get_path(grid, remaining_bytes[:mid + 1]) is None:
            # If blocked, the issue is in the first half
            right = mid - 1
        else:
            # If not blocked, move to the second half
            left = mid + 1

    # `left` now points to the index of the blocking byte
    blocking_byte = remaining_bytes[left]
    return blocking_byte


if __name__ == "__main__":
    grid = Grid.create(71, '.')
    bytes = parse_input(convert_fn=lambda b: list(map(int, b.split(","))))

    print(f"Solution to first puzzle: {solve(grid, bytes)}")
    print(f"Solution to first puzzle: {solve2(grid, bytes)}")
