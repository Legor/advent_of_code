# https://adventofcode.com/2024/day/4

from utils import Grid


def solve(grid):
    """Solve first part of the puzzle"""
    search_str = "XMAS"
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    count = 0
    for coord in grid.find("X"):
        # build words in all directions
        for x_mv, y_mv in directions:
            word = "".join(
                [grid[coord[0] + i * y_mv, coord[1] + i * x_mv][0] for i in range(4)]
            )
            # and check if they are "XMAS" or "SAMX"
            if word == search_str or word == search_str[::-1]:
                count += 1
    return count


def solve2(grid):
    """Solve second part of the puzzle"""
    search_str = "MAS"
    count = 0
    for coord in grid.find("A"):
        # only look in the diagonal directions, centered on "A"
        word1 = "".join(
            [
                grid[coord[0] - 1, coord[1] - 1][0],
                "A",
                grid[coord[0] + 1, coord[1] + 1][0],
            ]
        )
        word2 = "".join(
            [
                grid[coord[0] - 1, coord[1] + 1][0],
                "A",
                grid[coord[0] + 1, coord[1] - 1][0],
            ]
        )

        if (word1 == search_str or word1 == search_str[::-1]) and (
            word2 == search_str or word2 == search_str[::-1]
        ):
            count += 1
    return count


if __name__ == "__main__":
    grid = Grid.from_file()
    # pad border to handle edges lazily
    grid.pad_border("P", 3)

    print(f"Solution to first puzzle: {solve(grid)}")
    print(f"Solution to second  puzzle: {solve2(grid)}")
