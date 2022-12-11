from utils import input
import numpy as np


def solve(length):
    """Solve first or second part of the puzzle"""

    moves = {'R': (-1, 0), 'L': (1, 0), 'U': (0, 1), 'D': (0, -1)}
    visited = {(0, 0)}
    commands = input(convert_fn=lambda s: s.split())
    rope = [(0, 0) for i in range(length)]
    for c in commands:
        move = moves[c[0]]
        for step in range(int(c[1])):

            # move head
            rope[0] = (rope[0][0] + move[0], rope[0][1] + move[1])
            for i in range(1, len(rope)):
                pos_diff = (rope[i-1][0] - rope[i][0], rope[i-1][1] - rope[i][1])
                # move needed?
                if max(map(abs, pos_diff)) > 1:
                    rope[i] = (rope[i][0] + np.sign(pos_diff[0]), rope[i][1] + np.sign(pos_diff[1]))

            visited.add(rope[-1])

    return len(visited)


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve(2)}")
    print(f"Solution to second  puzzle: {solve(10)}")
