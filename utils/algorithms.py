from queue import PriorityQueue

from utils.graph import Graph
from typing import Optional


def dijkstra(graph: "Graph", start, end: Optional = None):
    """
    Solve the shortest path problem using Dijkstra's algorithm with a priority queue.

    Parameters:
        graph (Graph): The graph object containing nodes and edges.
        start: The starting node for the path search.
        end: The target node for the path search. If `None`, compute shortest paths
             to all reachable nodes from the start node.

    Returns:
        dict: A dictionary where each key is a node and the value is its predecessor
              in the shortest path. The dictionary can be used to reconstruct the
              shortest path from `start` to `end` or any other node.
    """

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
