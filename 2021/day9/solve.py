from utils import input, prod
import numpy as np
from scipy.ndimage.measurements import label


def conn_comp(cave_map, idx):
    x = (idx[0] + np.array((0, 0, -1, 1))).clip(0, cave_map.shape[1]-1)
    y = (idx[1] + np.array((-1, 1, 0, 0))).clip(0, cave_map.shape[0]-1)
    return cave_map[y, x]


def solve1():
    """Solve first puzzle"""
    cave_map = np.array(input(convert_fn=lambda r: [int(c) for c in r]))
    # pad array, to handle edge cases
    cave_map = np.pad(cave_map, (1, 1), 'constant', constant_values=(10, 10))
    risk = 0
    for x in range(1, cave_map.shape[1]-1):
        for y in range(1, cave_map.shape[0]-1):
            cc = conn_comp(cave_map, (x, y))
            print(cc)
            height = cave_map[y, x]
            if len([True for h in cc if h > height]) == 4:
                risk += height + 1
    return risk


def solve2():
    """Solve second puzzle"""
    cave_map = np.array(input(convert_fn=lambda r: [int(c) for c in r]))
    # 4 connected components
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    # use connected components labeling detection
    labels, ncomp = label(cave_map != 9, kernel)
    basins = []
    for n in range(1, ncomp+1):
        basins.append(np.count_nonzero(labels == n))

    return prod((sorted(basins, reverse=True)[:3]))


if __name__ == "__main__":
    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second puzzle: {solve2()}")
