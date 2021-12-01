from pathlib import Path
from itertools import combinations
from numpy import convolve


def conv_value_search(input_data, searched_value):
    for kernel_size in range(2, len(input_data)):
        conv_sum = list(convolve(input_data, [1] * kernel_size, 'valid'))
        try:
            sub_i = conv_sum.index(searched_value)
            subset = input_data[sub_i:sub_i+kernel_size]
            return min(subset), max(subset)
        except ValueError:
            continue


def find_encryption_error(input_data, window_size=25):
    """Return the index of the first number not following the encryption scheme."""
    for i in range(window_size, len(input_data)):
        comb = [sum(c) for c in combinations(input_data[i-window_size:i], 2)]
        if input_data[i] not in comb:
            return i


def solve_first(input_file):
    input_data = [int(x) for x in Path(input_file).read_text().splitlines()]
    return input_data[find_encryption_error(input_data, 25)]


def solve_second(input_file):
    input_data = [int(x) for x in Path(input_file).read_text().splitlines()]
    return sum(conv_value_search(input_data, solve_first(input_file)))


if __name__ == "__main__":
    input_file = 'input.txt'
    print(f"Solution to first puzzle: {solve_first(input_file)}")
    print(f"Solution to second  puzzle: {solve_second(input_file)}")
