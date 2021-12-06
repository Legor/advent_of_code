from utils import input
import numpy as np


def solve(no_diag=False):
    """Solve first or second puzzle"""
    r_in = input(convert_fn=lambda x: x.split('->'))
    r_in = [(c[0].split(','), c[1].split(',')) for c in r_in]
    r_in = [sorted([(int(c[0]), int(c[1])) for c in e]) for e in r_in]
    if no_diag:
        r_in = [c for c in r_in if c[0][0] == c[1][0] or c[0][1] == c[1][1]]
    max_xy = np.max(r_in, axis=0).max(axis=1)
    obstacles = np.zeros(max_xy + 1)
    for line in r_in:
        x1, y1, x2, y2 = *line[0], *line[1]
        d_x = x2 - x1
        d_y = y2 - y1
        if x1 == x2:
            obstacles[y1:y2+1, x1] += 1
        elif y1 == y2:
            obstacles[y1, x1:x2+1] += 1
        else:
            for x in range(x1, x2+1):
                y = int(y2 + d_y * (x - x2) / d_x)
                obstacles[y, x] += 1

    return np.count_nonzero(obstacles > 1)


if __name__ == "__main__":
    print(f"Solution to first puzzle: {solve(no_diag=True)}")
    print(f"Solution to second puzzle: {solve()}")
