import copy
import re
from pathlib import Path
from queue import PriorityQueue


class Grid:

    def __init__(self):
        self._data = None

    def __getitem__(self, item):
        y = slice(item[0], item[0] + 1, 1) if isinstance(item[0], int) else item[0]
        x = slice(item[1], item[1] + 1, 1) if isinstance(item[1], int) else item[1]
        vals = []
        for r in range(y.start, y.stop):
            for c in range(x.start, x.stop):
                vals.append(self._data[r][c])
        return vals[0] if len(vals) == 1 else vals

    def __setitem__(self, key, value):
        y = slice(key[0], key[0]+1, 1) if isinstance(key[0], int) else key[0]
        x = slice(key[1], key[1]+1, 1) if isinstance(key[1], int) else key[1]
        for r in range(y.start, y.stop):
            for c in range(x.start, x.stop):
                self._data[r][c] = value

    @property
    def width(self):
        assert self._data is not None
        return len(self._data[0])

    @property
    def height(self):
        assert self._data is not None
        return len(self._data)

    @property
    def shape(self):
        assert self._data is not None
        return self.height, self.width

    def pad_border(self, value, size):
        """Add border padding of size with the given value."""
        if isinstance(size, int):
            size = [size] * 4
        for i in range(size[0]):
            self._data.insert(0, [value] * self.width)
        for i in range(size[1]):
            self._data.insert(self.height, [value] * self.width)

        self._data = [[value] * size[2] + r for r in self._data]
        self._data = [r + [value] * size[2] for r in self._data]

    def add(self, val):
        """Add value to all elements."""
        self._data = [[c + val for c in row] for row in self._data]

    def apply_fn(self, fn):
        """Apply the given function element-wise."""
        self._data = [[fn(c) for c in r] for r in self._data]

    def find(self, val):
        """Return the indices of the given value."""
        return [(r, c) for r in range(self.height) for c in range(self.width) if self[(r, c)] == val]

    def print(self, file):

        for r in self._data:
            file.write("".join([str(s) for s in r])+'\n')
        file.write('\n')


    @classmethod
    def from_file(cls, file='input.txt', conv_fn=None):
        """Input -> matrice (grid, 2D-list).

       To parse a common grid-like input, e.g.:
        30373\n
        25512\n
        65332"""

        g = cls()
        g._data = input(file=file)
        if conv_fn is not None:
            g.apply_fn(conv_fn)
        return g

    @classmethod
    def zeros(cls, shape):
        """Return a Grid of given shape, with all values set to zero."""
        g = cls()
        if isinstance(shape, int):
            shape = (shape, shape)
        g._data = [[0] * shape[1] for r in range(shape[0])]
        return g

    @classmethod
    def cross(cls, sz):
        assert sz % 2, 'Mask size must be uneven.'
        g = cls.zeros(sz)
        g._data[sz // 2] = [1] * sz
        for i in range(sz):
            g._data[i][sz // 2] = 1
        return g


class Graph:

    def __init__(self):

        self._edges = {}

    def __getitem__(self, item):
        return self._edges[item[0]][item[1]]

    @property
    def n_vertices(self):
        return len(self._edges)

    def neighbors(self, vert_i):
        return list(self._edges[vert_i])

    def add_edge(self, u, v, weight=1):

        if u not in self._edges:
            self._edges[u] = {}

        if isinstance(v, int):
            v = [v]
        for k in v:
            self._edges[u][k] = weight

    def print(self):
        for e, n in self._edges.items():
            print(f'{e} -> {n}')

    @classmethod
    def from_grid(cls, grid: 'Grid', nb_mask: 'Grid', decision_fn):
        """Convert a grid into a Graph, using the supplied neighborhood mask and decision function.

            The mask defines the considered local neighborhood of each grid cell with the respective pixel in the middle.
            The mask is a binary mask, with 1 stating the element should be considered, and 0 otherwise.
            The decision_fn is executed on each potential grid-pair and should return a positive value (an edge weight)
            if the two graph nodes are considered neighbors.
        """
        new_graph = cls()

        # relative neighbor coordinates
        nb_coords = [(x - nb_mask.shape[0] // 2, y - nb_mask.shape[1] // 2) for x in range(nb_mask.shape[0])
                     for y in range(nb_mask.shape[1]) if nb_mask[(x, y)] == 1]
        nb_coords.remove((0, 0))
        for r in range(grid.height):
            for c in range(grid.width):
                for nb_coord in nb_coords:
                    # take care of grid borders
                    nb = (r+nb_coord[0], c+nb_coord[1])
                    if min(nb) < 0 or nb[0] >= grid.height or nb[1] >= grid.width:
                        continue
                    weight = decision_fn(grid[(r, c)], grid[nb])
                    if weight >= 0:
                        new_graph.add_edge((r, c), nb, weight)

        return new_graph


def dijkstra(graph: 'Graph', start, end):
    """Solve shortest path using Dijkstra and a priority queue."""

    dist = {v: 10000 for v in graph._edges}
    dist[start] = 0
    previous = {v: None for v in graph._edges}
    visited = []

    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():

        (_, cur_v) = pq.get()
        if end is not None and cur_v == end:
            break
        visited.append(cur_v)

        for nb_i in graph.neighbors(cur_v):
            if nb_i not in visited:
                cost = dist[cur_v] + 1
                if cost < dist[nb_i]:
                    pq.put((cost, nb_i))
                    dist[nb_i] = cost
                    previous[nb_i] = cur_v

    return previous


def input(file='input.txt', convert_fn=None, split_on='\n'):
    lines = Path(file).read_text()
    if split_on:
        lines = lines.split(split_on)
    if convert_fn:
        lines = [convert_fn(x) for x in lines]
    return lines
def test_results(solve1, solve2, file='solutions.txt'):
    if Path(file).exists():
        solutions = input(file, convert_fn=int)
        print('\u2705' if solve1 == solutions[0] else '\u274C ', f' {solve1} == {solutions[0]}')
        print('\u2705' if solve2 == solutions[1] else '\u274C ', f' {solve2} == {solutions[1]}')
    else:
        print('Skipping test, no solutions found.')

def get_mask(arr, cond):
    """For a 2-d list return a binary array of the same shape (a mask) according to the given condition"""

    mask = copy.deepcopy(arr)
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            mask[i][j] = cond(arr[i][j])
    return mask


def l_to_i(li):
    """Map all elements of a list to int"""
    return list(map(int, li))


def chunks(xs, n):
    """split list into chunks of size n"""
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))


def bits_to_dec(arr):
    """
    [False, True, True] --> 3
    [1, 0, 1, 0] --> 6
    "0111" --> 7
    [1, '0', 0, False, '1', True] --> 35
    """
    return int("".join([str(int(x)) for x in arr]), 2)


def prod(numbers):
    """Return the product of all numbers in the given list."""
    y = 1
    for x in numbers:
        y *= x
    return y


def sign(x):
    return -1 if x < 0 else 1


def substring_idx(text, substring):
    """Return the starting indices of all occurrences of substring in text."""
    pattern = re.escape(substring)
    return [match.start() for match in re.finditer(pattern, text)]
