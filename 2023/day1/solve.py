from utils import parse_input, substring_idx


def solve():
    """Solve first part of the puzzle"""
    # only keep the digits of each line
    numbers = parse_input(convert_fn=lambda s: "".join(filter(str.isdigit, s)))
    #  concat first and last digit, convert to int, calculate sum
    return sum(map(int, [n[0]+n[-1] for n in numbers if n]))


def solve3():
    """Solve second part of the puzzle"""

    # produce a map for different string representations to ints (e.g. 'one': 1, '1': 1)
    str_digit_map = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    str_digit_map = {s: str(i) for i, s in enumerate(str_digit_map, start=1)}
    str_digit_map.update({str(i): str(i) for i in range(1, 10)})

    result = 0
    for line in parse_input():
        # in each line find the starting indices for each number string
        findings = {}
        for s, v in str_digit_map.items():
            findings.update({i: v for i in substring_idx(line, s)})
        # the minimum and maximum indices correspond to the first and last digit in the string
        min_idx, max_idx = min(findings), max(findings)
        # concat digits and sum up
        result += int("".join((findings[min_idx], findings[max_idx])))

    return result

def solve2():
    """Solve second part of the puzzle"""

    # produce a map for different string representations to ints (e.g. 'one': 1, '1': 1)
    str_digit_map = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    str_digit_map = {s: str(i) for i, s in enumerate(str_digit_map, start=1)}
    str_digit_map.update({str(i): str(i) for i in range(1, 10)})

    result = 0
    for line in parse_input():
        # in each line find the starting indices for each number string
        findings = {}
        for s, v in str_digit_map.items():
            findings.update({i: v for i in substring_idx(line, s)})
        # the minimum and maximum indices correspond to the first and last digit in the string
        min_idx, max_idx = min(findings), max(findings)
        # concat digits and sum up
        result += int("".join((findings[min_idx], findings[max_idx])))

    return result


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve2()}")
