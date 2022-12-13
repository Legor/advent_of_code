from utils import Grid, Graph, dijkstra


def solve(target=None):

    input_grid = Grid.from_file()
    # get start and end coordinates
    start = input_grid.find('S')[0]
    end = input_grid.find('E')[0]
    input_grid.apply_fn(ord)
    input_grid[start] = ord('a')
    input_grid[end] = ord('z')

    nb_mask = Grid.cross(3)
    graph = Graph.from_grid(input_grid, nb_mask, decision_fn=lambda x, y: 1 if x+1 >= y else -1)

    previous = dijkstra(graph, start, end)

    path = []
    u = end
    while u is not None:
        # search up to starting point
        if target is None:
            if u == start:
                path.append(start)
                break
        # search up to specified elevation level
        elif input_grid[u] == ord(target):
            break

        u = previous[u]
        path.append(u)

    return len(path)-1


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second puzzle: {solve('a')}")
