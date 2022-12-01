from utils import input


def solve(top_n=1):
    """Solve first or second part of the puzzle"""
    raw_input = input(split=False)
    # split on empty lines, convert each number to int, calculate sum
    splits = [sum(list(map(int, sp.split()))) for sp in raw_input.split('\n\n')]
    splits = sorted(splits, reverse=True)
    return sum(splits[:top_n])


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve(3)}")