from copy import deepcopy

from utils.parsing import parse_input
from typing import Union
from pathlib import Path

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
        y = slice(
            y.start if y.start is not None else 0,
            y.stop if y.stop is not None else len(self._data),
            y.step if y.step is not None else 1,
        )

        # Handle slice or integer for columns
        x = slice(item[1], item[1] + 1, 1) if isinstance(item[1], int) else item[1]
        x = slice(
            x.start if x.start is not None else 0,
            x.stop if x.stop is not None else len(self._data[0]),
            x.step if x.step is not None else 1,
        )

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
        y = slice(key[0], key[0] + 1, 1) if isinstance(key[0], int) else key[0]
        x = slice(key[1], key[1] + 1, 1) if isinstance(key[1], int) else key[1]
        for r in range(y.start, y.stop):
            for c in range(x.start, x.stop):
                self._data[r][c] = value

    def __eq__(self, other):
        return False not in [
            self._data[y][x] == other._data[y][x]
            for y in range(self.shape[0])
            for x in range(self.shape[1])
        ]

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
        self._data = [
            [value] * size[2]
            + (list(r) if isinstance(r, str) else r)
            + [value] * size[3]
            for r in self._data
        ]

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
        return [
            (r, c)
            for r in range(self.height)
            for c in range(self.width)
            if val in self[(r, c)]
        ]

    def neighborhood(self, idx: tuple):
        """Return the values of the neighborhood (8-connected) of the given index."""
        y, x = idx
        return Grid(
            self[
                max(0, y - 1) : min(self.height, y + 2),
                max(0, x - 1) : min(self.width, x + 2),
            ]
        )

    def flatten(self):
        return [self._data[r][c] for r in range(self.height) for c in range(self.width)]

    def write(self, file_path: Union[str, Path]):
        file_path = Path(file_path)
        if file_path.exists():
            raise IOError(f"Not allowed to overwrite file: {file_path}")
        with open(file_path, "w") as out:
            for r in self._data:
                out.write("".join([str(s) for s in r]) + "\n")

    def __str__(self):
        return "\n".join([("".join([str(s) for s in r])) for r in self._data])

    @classmethod
    def from_file(cls, file="input.txt", conv_fn=None):
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
    def create(cls, shape: Union[int, tuple[int, int]], value=0):
        """Return a Grid of given shape, with all values set to a given value (default 0)."""
        g = cls()
        if isinstance(shape, int):
            shape = (shape, shape)
        g._data = [[value] * shape[1] for _ in range(shape[0])]
        return g

    @classmethod
    def cross(cls, sz):
        assert sz % 2, "Mask size must be uneven."
        g = cls.create(sz)
        g._data[sz // 2] = [1] * sz
        for i in range(sz):
            g._data[i][sz // 2] = 1
        return g

