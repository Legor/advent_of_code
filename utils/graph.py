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
        visited = []
        queue = set([(start_node, 0)])  # (Node, Distance)

        while queue:
            node, steps = queue.pop()
            if steps == max_steps:
                # visited.add(node)
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
            print(f"{e} -> {n}")

    @classmethod
    def from_grid(cls, grid: "Grid", nb_mask: "Grid", decision_fn, repeat_grid=None):
        """Convert a grid into a Graph, using the supplied neighborhood mask and decision function.

        The mask defines the considered local neighborhood of each grid cell with the respective pixel in the middle.
        The mask is a binary mask, with 1 stating the element should be considered, and 0 otherwise.
        The decision_fn is executed on each potential grid-pair and should return a positive value (an edge weight)
        if the two graph nodes are considered neighbors.
        repeat_grid controls if the grid is allowed to repeat, i.e. nodes will connect to neighbors even if they
        were beyond the grid
        """

        def __check_coords(coords):
            return (
                min(coords) >= 0
                and coords[0] < grid.height
                and coords[1] >= 0
                and coords[1] < grid.width
            )

        new_graph = cls()
        # map coords to distinct indices
        coord_i = []
        # relative neighbor coordinates
        nb_coords = [
            (x - nb_mask.shape[0] // 2, y - nb_mask.shape[1] // 2)
            for x in range(nb_mask.shape[0])
            for y in range(nb_mask.shape[1])
            if nb_mask[x, y][0] == 1
        ]
        nb_coords.remove((0, 0))
        for r in range(grid.height):
            for c in range(grid.width):
                neighbors = [
                    (r + nb_coord[0], c + nb_coord[1]) for nb_coord in nb_coords
                ]
                if not repeat_grid:
                    neighbors = [nb for nb in neighbors if __check_coords(nb)]
                else:
                    neighbors = [
                        (nb[0] % grid.height, nb[1] % grid.width) for nb in neighbors
                    ]
                for nb in neighbors:
                    weight = decision_fn(grid[(r, c)], grid[nb])
                    if weight > 0:
                        if (r, c) not in coord_i:
                            coord_i.append((r, c))
                        if nb not in coord_i:
                            coord_i.append(nb)
                        # new_graph.add_edge(coord_i.index((r, c)), coord_i.index(nb), weight, grid[(r, c)][0])
                        new_graph.add_edge((r, c), [nb], weight, grid[(r, c)][0])

        return new_graph
