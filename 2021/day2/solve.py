from utils import parse_input
import numpy as np


def solve1():
    """Solve first puzzle"""
    r_in = parse_input(convert_fn=lambda x: x.split())
    mv = {'forward': (0, 1), 'down': (1, 0),  'up': (-1, 0)}
    # multiply each movement vector with length
    r_in = [np.array(mv[x[0]]) * int(x[1]) for x in r_in]
    return np.prod(sum(r_in))


def solve2():
    """Solve second puzzle"""
    r_in = parse_input(convert_fn=lambda x: x.split())
    mv = {'forward': (1, 1, 0), 'down': (0, 0, 1), 'up': (0, 0, -1)}
    r_in = [np.array(mv[x[0]]) * int(x[1]) for x in r_in]

    aim = 0
    yx = (0, 0)
    for r in r_in:
        aim += r[2]
        yx = (yx[0] + aim * r[0], yx[1] + r[1])

    return yx[0] * yx[1]





if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second puzzle: {solve2()}")
