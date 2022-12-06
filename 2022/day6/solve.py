from utils import input
from collections import Counter


def solve(msg_length=4):
    """Solve first part of the puzzle"""
    game_input = input()

    for line in game_input:
        for i in range(0, len(line)):
            if max(Counter(line[i:i+msg_length]).values()) == 1:
                return i+msg_length


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve(14)}")
