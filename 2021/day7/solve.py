from utils import parse_input
import numpy as np


def solve1():
    """Solve first puzzle"""
    r_in = np.array([int(n) for n in parse_input(convert_fn=lambda x: x.split(','))[0]])
    fuel = []
    for i in range(np.max(r_in)+1):
        fuel.append(np.sum(np.abs(r_in - i)))
    return np.min(fuel)


def solve2():
    """Solve first puzzle"""
    r_in = np.array([int(n) for n in parse_input(convert_fn=lambda x: x.split(','))[0]])
    fuel = []
    costs = list(range(1, np.max(r_in)+1))
    for i in range(np.max(r_in)+1):
        fuel.append(sum([sum(costs[:c]) for c in np.abs(r_in - i)]))
    return np.min(fuel)


if __name__ == "__main__":
    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second puzzle: {solve2()}")
