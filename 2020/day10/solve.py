from pathlib import Path
from utils import prod
import re


def prepare_data(input_file = 'input.txt'):
    input_data = [int(x) for x in Path(input_file).read_text().splitlines()]
    input_data += [0, max(input_data) + 3]
    input_data.sort()
    return input_data


def solve_first():
    input_data = prepare_data()
    j_diff = [input_data[i + 1] - input_data[i] for i in range(len(input_data) - 1)]
    return j_diff.count(1) * j_diff.count(3)


def solve_second():
    def n_combinations(x):
        if x == 2:
            return 2
        if x == 3:
            return 4
        else:
            return n_combinations(x - 1) * 2 - 1

    input_data = prepare_data()
    j_diff = [input_data[i + 1] - input_data[i] for i in range(len(input_data) - 1)]
    j_diff.insert(0, 3)
    # convert array of differences into string
    diff_str = "".join([str(x) for x in j_diff])
    # extract the 1-difference fields
    one_counts = re.compile('(?=3(1{2,})3)').findall(diff_str)
    return prod([n_combinations(len(c)) for c in one_counts])


if __name__ == "__main__":
    print(f"Solution to first puzzle: {solve_first()}")
    print(f"Solution to second  puzzle: {solve_second()}")
