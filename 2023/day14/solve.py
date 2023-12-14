from utils import  Grid


def move(grid, tilt):

    rocks = grid.find('O')
    # use sorted/reverse order of rocks for easier processing
    rocks = rocks[::-1] if -1 not in tilt else rocks
    for rock in rocks:
        while True:
            next_y, next_x = rock[0] + tilt[0], rock[1] + tilt[1]
            # collision conditions
            if not 0 <= next_y < grid.shape[0] or not 0 <= next_x < grid.shape[1] or grid[next_y, next_x][0] != '.':
                break
            # move rock
            grid[rock[0], rock[1]] = '.'
            grid[next_y, next_x] = 'O'
            rock = next_y, next_x
    return grid


def weight(grid):
    return sum([grid.shape[0] - rock[0] for rock in grid.find('O')])


def solve2(n_cycles=1000000000):
    """Solve second puzzle"""
    tilts = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    grid = Grid.from_file()
    # track intermediate grids for cycle detection
    grids = []
    for cycle in range(n_cycles):
        # repetition detected
        if grid in grids:
            repeat_start = grids.index(grid)
            # compute grid index at end of loop
            end_idx = repeat_start+((n_cycles-cycle) % (cycle - repeat_start))
            return weight(grids[end_idx])
        # track intermediate grids to check for repetition
        grids.append(Grid(grid._data))
        for tilt in tilts:
            move(grid, tilt)


if __name__ == "__main__":
    print(f"Solution to first puzzle: {weight(move(Grid.from_file(), (-1, 0)))}"),
    print(f"Solution to second puzzle: {solve2()}")
