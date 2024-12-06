import copy
import re
import math
from pathlib import Path
from functools import reduce
from queue import PriorityQueue
from copy import deepcopy
from collections import deque


class Grid:

    def __init__(self, data=None):
        if data is None:
            self._data = None
        else:
            self._data = deepcopy(data)

    def __getitem__(self, item):
        # Handle single integer indexing
        if isinstance(item, int):
            return self._data[item]

        # Handle slice or integer for rows
        y = slice(item[0], item[0] + 1, 1) if isinstance(item[0], int) else item[0]
        y = slice(y.start if y.start is not None else 0,
                  y.stop if y.stop is not None else len(self._data),
                  y.step if y.step is not None else 1)

        # Handle slice or integer for columns
        x = slice(item[1], item[1] + 1, 1) if isinstance(item[1], int) else item[1]
        x = slice(x.start if x.start is not None else 0,
                  x.stop if x.stop is not None else len(self._data[0]),
                  x.step if x.step is not None else 1)

        # Extract the values
        vals = []
        for r in range(y.start, y.stop, y.step):
            row = [self._data[r][c] for c in range(x.start, x.stop, x.step)]
            vals.append(row)

        # Return the result
        if len(vals) == 1:
            return vals[0]  # Return a single list if one row/column
        return vals

    def __setitem__(self, key, value):
        y = slice(key[0], key[0]+1, 1) if isinstance(key[0], int) else key[0]
        x = slice(key[1], key[1]+1, 1) if isinstance(key[1], int) else key[1]
        for r in range(y.start, y.stop):
            for c in range(x.start, x.stop):
                self._data[r][c] = value

    def __eq__(self, other):
        return False not in [self._data[y][x] == other._data[y][x] for y in range(self.shape[0]) for x in range(self.shape[1])]

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

        # Pad top and bottom
        for _ in range(size[0]):  # Top padding
            self._data.insert(0, [value] * self.width)
        for _ in range(size[1]):  # Bottom padding
            self._data.append([value] * self.width)

        # Pad left and right
        self._data = [[value] * size[2] + (list(r) if isinstance(r, str) else r) + [value] * size[3] for r in
                      self._data]

    def transpose(self):
        # Convert strings to lists if necessary
        grid = [list(row) if isinstance(row, str) else row for row in self._data]

        # Transpose the grid
        return Grid(list(map(list, zip(*grid))))

    def add(self, val):
        """Add value to all elements."""
        self._data = [[c + val for c in row] for row in self._data]

    def apply_fn(self, fn):
        """Apply the given function element-wise."""
        self._data = [[fn(c) for c in r] for r in self._data]

    def find(self, val):
        """Return the indices of the given value."""
        return [(r, c) for r in range(self.height) for c in range(self.width) if val in self[(r, c)]]

    def neighborhood(self, idx: tuple):
        """Return the values of the neighborhood (8-connected) of the given index."""
        indices = []
        y, x = idx
        return Grid(self[max(0, y-1):min(self.height, y+2), max(0, x-1):min(self.width, x+2)])

    def flatten(self):
        return [self._data[r][c] for r in range(self.height) for c in range(self.width)]

    def print(self, file):

        for r in self._data:
            file.write("".join([str(s) for s in r])+'\n')
        file.write('\n')

    def __str__(self):
        return '\n'.join([("".join([str(s) for s in r])) for r in self._data])

    @classmethod
    def from_file(cls, file='input.txt', conv_fn=None):
        """Input -> matrice (grid, 2D-list).

       To parse a common grid-like input, e.g.:
        30373\n
        25512\n
        65332"""

        g = cls()
        g._data = parse_input(file=file, convert_fn=list)
        if conv_fn is not None:
            g.apply_fn(conv_fn)
        return g

    @classmethod
    def create(cls, shape, value=0):
        """Return a Grid of given shape, with all values set to zero."""
        g = cls()
        if isinstance(shape, int):
            shape = (shape, shape)
        g._data = [[value] * shape[1] for r in range(shape[0])]
        return g

    @classmethod
    def cross(cls, sz):
        assert sz % 2, 'Mask size must be uneven.'
        g = cls.create(sz)
        g._data[sz // 2] = [1] * sz
        for i in range(sz):
            g._data[i][sz // 2] = 1
        return g


class Graph:
    """A simple implementation of a graph data structure supporting directed graphs with optional weighted edges."""

    def __init__(self):

        self._edges = {}
        self._values = {}

    def __getitem__(self, item):
        """Enables getting the weight of the edge between two vertices.

        Args:
            item (tuple): A tuple (u, v) representing an edge from vertex u to vertex v.

        Returns:
            The weight of the edge from u to v.
        """
        return self._edges[item[0]][item[1]]

    @property
    def n_vertices(self):
        """Returns the number of vertices in the graph.

        Returns:
            int: The count of vertices.
        """
        return len(self._edges)

    def neighbors(self, vert_i):
        """Retrieves the neighboring vertices of a given vertex.

        Args:
            vert_i: The vertex for which neighbors are requested.

        Returns:
            list: A list of neighboring vertices of vert_i.
        """
        return list(self._edges[vert_i])

    def add_edge(self, u, v, weight=1, value=None):
        """Adds an edge from vertex u to vertex v with an optional weight.

        Examples:
            g = Graph()
            g.add_edge(1, 2)  # Adds an edge from vertex 1 to vertex 2
            g.add_edge(1, 3)  # Adds another edge from vertex 1 to vertex 3
            g.add_edge(1, [2, 3, 4])  # Adds edges from vertex 1 to vertices 2, 3, and 4

        Args:
            u: The starting vertex of the edge.
            v: The ending vertex of the edge. Can be a single vertex or a list of vertices.
            weight (int, optional): The weight of the edge. Defaults to 1.
        """

        if u not in self._edges:
            self._edges[u] = {}
        if u not in self._values:
            self._values[u] = value

        if isinstance(v, int):
            v = [v]
        for k in v:
            self._edges[u][k] = weight

    def count_reachable_nodes(self, start_node, max_steps):
        """Count the number of nodes reachable after the exact amount of max_steps."""
        #visited = set()
        visited = []
        queue = set([(start_node, 0)])  # (Node, Distance)

        while queue:
            node, steps = queue.pop()
            if steps == max_steps:
                #visited.add(node)
                visited.append(node)
            else:
                for neighbor in self.neighbors(node):
                    queue.add((neighbor, steps + 1))

        return len(visited)

    def index(self, value):
        """Return the node indices for a given value."""
        for n, v in self._values.items():
            if v == value:
                return n

    def print(self):
        """Prints a representation of the graph. Lists each vertex and its corresponding edges with weights."""
        for e, n in self._edges.items():
            print(f'{e} -> {n}')

    @classmethod
    def from_grid(cls, grid: 'Grid', nb_mask: 'Grid', decision_fn, repeat_grid=None):
        """Convert a grid into a Graph, using the supplied neighborhood mask and decision function.

            The mask defines the considered local neighborhood of each grid cell with the respective pixel in the middle.
            The mask is a binary mask, with 1 stating the element should be considered, and 0 otherwise.
            The decision_fn is executed on each potential grid-pair and should return a positive value (an edge weight)
            if the two graph nodes are considered neighbors.
            repeat_grid controls if the grid is allowed to repeat, i.e. nodes will connect to neighbors even if they
            were beyond the grid
        """
        def __check_coords(coords):
            return min(coords) >= 0 and coords[0] < grid.height and coords[1] >= 0 and coords[1] < grid.width

        new_graph = cls()
        # map coords to distinct indices
        coord_i = []
        # relative neighbor coordinates
        nb_coords = [(x - nb_mask.shape[0] // 2, y - nb_mask.shape[1] // 2) for x in range(nb_mask.shape[0])
                     for y in range(nb_mask.shape[1]) if nb_mask[x, y][0] == 1]
        nb_coords.remove((0, 0))
        for r in range(grid.height):
            for c in range(grid.width):
                neighbors = [(r+nb_coord[0], c+nb_coord[1]) for nb_coord in nb_coords]
                if not repeat_grid:
                    neighbors = [nb for nb in neighbors if __check_coords(nb)]
                else:
                    neighbors = [(nb[0]%grid.height, nb[1]%grid.width) for nb in neighbors]
                for nb in neighbors:
                    weight = decision_fn(grid[(r, c)], grid[nb])
                    if weight > 0:
                        if (r, c) not in coord_i:
                            coord_i.append((r, c))
                        if nb not in coord_i:
                            coord_i.append(nb)
                        #new_graph.add_edge(coord_i.index((r, c)), coord_i.index(nb), weight, grid[(r, c)][0])
                        new_graph.add_edge((r, c), [nb], weight, grid[(r, c)][0])

        return new_graph


class TreeNode:
    """A node in a binary tree."""

    def __init__(self, value):
        """
        Initialize a tree node.

        Args:
            value: The value of the node.
        """
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    """A simple binary tree."""

    def __init__(self):
        """
        Initialize an empty binary tree.
        """
        self.root = None
        self.leafs = {}

    def __getitem__(self, item):
        if item in self.leafs:
            return self.leafs[item]

    def add_leaf(self, value, children=(None, None)):
        """
        Add a node to the tree with optional left and right children.

        Args:
            value: The value of the node to add.
            children (tuple): A tuple (left_child_value, right_child_value).
                              Use None for no child.

        Returns:
            The newly created node.
        """
        if value not in self.leafs:
            self.leafs[value] = TreeNode(value)

        node = self.leafs[value]

        if not self.root:
            self.root = node

        left_value, right_value = children

        if left_value is not None:
            if left_value not in self.leafs:
                self.leafs[left_value] = TreeNode(left_value) if left_value != value else node
            node.left = self.leafs[left_value]

        if right_value is not None:
            if right_value not in self.leafs:
                self.leafs[right_value] = TreeNode(right_value) if right_value != value else node
            node.right = self.leafs[right_value]

        return node

    def left(self, parent_value):
        """
        Get the left child of a given node.

        Args:
            parent_value: The value of the parent node.

        Returns:
            The child node, or None if the child does not exist.
        """
        parent_node = self.leafs.get(parent_value)
        if parent_node:
            return parent_node.left
        return None

    def right(self, parent_value):
        """
        Get the right child of a given node.

        Args:
            parent_value: The value of the parent node.

        Returns:
            The child node, or None if the child does not exist.
        """
        parent_node = self.leafs.get(parent_value)
        if parent_node:
            return parent_node.right
        return None

    def print(self, node, level=0, prefix="Root: ", visited=None):
        """
        Print the tree in a hierarchical format.

        Args:
            node: The current node to print.
            level: The current level in the tree.
            prefix: The prefix to print before the node value.
        """
        if node is None:
            return

        if visited is None:
            visited = set()

            # Check for circular dependency
        if node in visited:
            print(" " * (level * 4) + prefix + str(node.value) + " (circular)")
            return
        else:
            visited.add(node)

        print(" " * (level * 4) + prefix + str(node.value))
        self.print(node.left, level + 1, "L--- ", visited)
        self.print(node.right, level + 1, "R--- ", visited)


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


def dfs_longest_path(graph, start, end):
    def dfs(node):
        visited.add(node)
        current_path.append(node)

        if node == end:
            nonlocal longest_path
            if len(current_path) > len(longest_path):
                longest_path = current_path.copy()
        else:
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor)

        current_path.pop()
        visited.remove(node)

    visited = set()
    current_path = []
    longest_path = []

    dfs(start)

    if not longest_path:
        return None  # No path exists
    else:
        return longest_path


def parse_input(file='input.txt', convert_fn=None, split_on='\n'):
    lines = Path(file).read_text()
    if split_on:
        lines = lines.split(split_on)
    if convert_fn:
        lines = [convert_fn(x) for x in lines]
    return lines
def test_results(solve1, solve2, file='solutions.txt'):
    if Path(file).exists():
        solutions = parse_input(file, convert_fn=int)
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

def lcm(a, b):
    """Calculate the least common multiple (LCM) for two numbers."""
    return abs(a * b) // math.gcd(a, b)

def find_lcm(numbers: list):
    """Calculate the least common multiple (LCM) for a list of numbers."""
    return reduce(lcm, numbers)

def get_nb_indices(y, x):
    """Generate a list of 2d neighborhood indices (8-connected) for a given center coordinate.
    The center coordinate itself is excluded."""
    return [(j, i) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2) if (j, i) != (y, x)]


def substring_idx(text: str, substring: str):
    """Return the starting indices of all occurrences of substring in text."""
    pattern = re.escape(substring)
    return [match.start() for match in re.finditer(pattern, text)]


def find_pattern_in_lines(lines: list, pattern: str):
    """Return the matches of all provided regular expressions in all given lines."""
    return [list(re.finditer(pattern, line)) for line in lines]


