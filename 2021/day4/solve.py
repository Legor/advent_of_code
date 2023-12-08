from utils import parse_input
from collections import OrderedDict
import numpy as np


def solve(won_board_i):
    """Solve first or second puzzle"""
    BOARD_SIZE = 5

    r_in = parse_input()
    numbers = [int(n) for n in r_in[0].split(',')]
    boards = [r_in[i:i + BOARD_SIZE] for i in range(2, len(r_in) - (BOARD_SIZE-1), (BOARD_SIZE+1))]
    boards = [[row.split() for row in b] for b in boards]
    boards = list(map(lambda x: np.array([[int(n) for n in row] for row in x]), boards))
    # mask arrays to mark all numbers crossed, per board
    hits = [np.zeros(b.shape, dtype=np.bool) for b in boards]

    # remember which boards have won, with which number
    won_boards = OrderedDict()
    for n in numbers:
        # mark all boards that have not finished yet
        for i, h in enumerate(hits):
            if i not in won_boards:
                hits[i] = np.bitwise_or(h, boards[i] == n)
        # check for complete row or column
        for i, h in enumerate(hits):
            if BOARD_SIZE in np.count_nonzero(h, axis=0) or 5 in np.count_nonzero(h, axis=1):
                # ummarked numbers
                if i not in won_boards:
                    won_boards[i] = n

    # the board_id of the i-th won board and the number won with
    b_id, won_n = list(won_boards.keys())[won_board_i], list(won_boards.values())[won_board_i]
    return np.sum(boards[b_id][hits[b_id] == False]) * won_n


if __name__ == "__main__":
    print(f"Solution to first puzzle: {solve(0)}")
    print(f"Solution to second puzzle: {solve(-1)}")
