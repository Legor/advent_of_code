# https://adventofcode.com/2024/day/5

from utils import parse_input
from collections import defaultdict, deque

def get_rules_and_updates():
    rules, updates = parse_input(split_on="\n\n")
    rules = [tuple(map(int, rule.split('|'))) for rule in rules.splitlines()]
    updates = [list(map(int, update.split(','))) for update in updates.splitlines()]
    return rules, updates

def is_valid_update(update, rules):
    # Create a mapping of page numbers to their indices in the update
    index_map = {page: i for i, page in enumerate(update)}
    for x, y in rules:
        if x in index_map and y in index_map:
            # Check if x comes before y
            if index_map[x] >= index_map[y]:
                return False
    return True


def solve(rules, updates):
    """Solve first part of the puzzle"""
    valid_updates = []
    for update in updates:
        if is_valid_update(update, rules):
            valid_updates.append(update)
    # Find the middle page of each valid update and sum them
    middle_pages_sum = sum(update[len(update) // 2] for update in valid_updates)
    return middle_pages_sum


def reorder_update(update, rules):
    # Create a directed graph of dependencies
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    for x, y in rules:
        if x in update and y in update:
            graph[x].append(y)
            in_degree[y] += 1
            if x not in in_degree:
                in_degree[x] = 0

    # Perform topological sort
    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_update = []
    while queue:
        node = queue.popleft()
        sorted_update.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update


def solve2(rules, updates):

    invalid_updates = [update for update in updates if not is_valid_update(update, rules)]

    # Correct invalid updates and compute middle pages
    corrected_updates = [reorder_update(update, rules) for update in invalid_updates]
    invalid_middle_sum = sum(update[len(update) // 2] for update in corrected_updates)

    return invalid_middle_sum

if __name__ == "__main__":
    rules, updates = get_rules_and_updates()
    print(f"Solution to first puzzle: {solve(rules, updates)}")
    print(f"Solution to second puzzle: {solve2(rules, updates)}")
