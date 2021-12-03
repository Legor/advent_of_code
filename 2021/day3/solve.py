from utils import input, bits_to_dec
import numpy as np


def solve1():
    """Solve first puzzle"""
    # parse to matrix
    r_in = np.array(input(convert_fn=lambda x: [int(n) for n in list(x)]))
    # get dominant bit per column
    epsilon = np.count_nonzero(r_in, axis=0) > (r_in.shape[0] / 2)
    gamma = np.invert(epsilon)
    return bits_to_dec(epsilon) * bits_to_dec(gamma)


def rec_search(in_data, c_i, comp_op):
    if in_data.shape[0] == 1:
        return in_data
    dom = comp_op(in_data[:, c_i])
    return rec_search(in_data[in_data[:, c_i] == dom], c_i+1, comp_op)


def solve2():
    """Solve second puzzle"""
    # parse to matrix
    r_in = np.array(input(convert_fn=lambda x: [int(n) for n in list(x)]))
    oxy = rec_search(r_in, 0, lambda x: np.count_nonzero(x) >= (len(x) / 2))[0]
    scrub = rec_search(r_in, 0, lambda x: np.count_nonzero(x) < (len(x) / 2))[0]
    # convert to bit patterns to 16 bit format for np.packbits
    return bits_to_dec(oxy) * bits_to_dec(scrub)


if __name__ == "__main__":
    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second puzzle: {solve2()}")
