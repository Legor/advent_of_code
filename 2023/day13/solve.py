from utils import parse_input, Grid


def find_reflection_line(grid, allowed_smudges=0):
    num_rows = grid.shape[0]
    num_cols = grid.shape[1]

    # Iterate through possible reflection lines
    for mid in range(1, num_cols):
        left, right = grid[:, :mid], grid[:, mid:]
        misses = [left[r_i][::-1][c_i] != right[r_i][c_i] for r_i in range(num_rows)
                  for c_i in range(min(len(left[0]), len(right[0])))]
        if sum(misses) == allowed_smudges:
            return mid

    return 0


if __name__ == "__main__":

    grids = parse_input(split_on='\n\n')
    grids = [Grid(g.split('\n')) for g in grids]

    result1, result2 = 0, 0
    for g in grids:
        result1 += find_reflection_line(g) + 100 * find_reflection_line(g.transpose())
        result2 += find_reflection_line(g, 1) + 100 * find_reflection_line(g.transpose(), 1)

    print(f"Solution to first puzzle: {result1}")
    print(f"Solution to second puzzle: {result2}")

