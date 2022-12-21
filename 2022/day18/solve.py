from utils import input
import numpy as np
import scipy.ndimage
from skimage.morphology import flood_fill


def surface_area(node_coords, grid):

    # kernel for 4-region
    k = np.zeros((3, 3, 3))
    k[1, 1, :] = -1
    k[1, :, 1] = -1
    k[:, 1, 1] = -1
    k[1, 1, 1] = 6

    # will yield the number of free 4-connected neighbors for each node
    grid = scipy.ndimage.convolve(grid, k, mode='constant')
    return int(sum([grid[c[0] - 1, c[1] - 1, c[2] - 1] for c in node_coords]))


def solve(fill_holes=False):

    cubes = input(convert_fn=lambda x: [int(c) for c in x.split(',')])
    grid = np.zeros([np.max(cubes)] * 3)
    for c in cubes:
        grid[c[0]-1, c[1]-1, c[2]-1] = 1

    if fill_holes:
        # fill/detect the air regions (need padding because stone may touch grid border)
        grid = flood_fill(np.pad(grid, 1), (0, 0, 0), -1, connectivity=1)
        # remove padding (to keep original index)
        grid = grid[1:-1, 1:-1, 1:-1]
        # fill the holes
        grid[grid == 0] = 1
        # reset air region
        grid[grid == -1] = 0

    return surface_area(cubes, grid)


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second puzzle: {solve(fill_holes=True)}")
