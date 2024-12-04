# https://adventofcode.com/2024/day/2

from utils import parse_input


def check_report(report):
    diffs = [report[i] - report[i + 1] for i in range(len(report) - 1)]
    if 0 in diffs or max(map(abs, diffs)) > 3:
        return False
    signs = [d > 0 for d in diffs]
    if sum(signs) != 0 and sum(signs) != len(diffs):
        return False
    return True


def solve(reports):
    """Solve first part of the puzzle"""
    return sum([check_report(report) for report in reports])


def solve2(reports):
    """Solve second part of the puzzle"""
    check_again = [report for report in reports if not check_report(report)]
    correct = len(reports) - len(check_again)
    for report in check_again:
        # check again with removed level
        for i in range(len(report)):
            tmp = report.copy()
            del tmp[i]
            if check_report(tmp):
                correct += 1
                break

    return correct


if __name__ == "__main__":
    reports = parse_input(convert_fn=lambda line: list(map(int, str.split(line))))
    print(f"Solution to first puzzle: {solve(reports)}")
    print(f"Solution to second  puzzle: {solve2(reports)}")
