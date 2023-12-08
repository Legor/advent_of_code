from utils import parse_input, test_results


def solve(top_n=1):
    """Solve first or second part of the puzzle"""
    raw_input = parse_input(split_on='\n\n')
    #  convert each number to int, calculate sum
    splits = [sum(list(map(int, sp.split()))) for sp in raw_input]
    splits = sorted(splits, reverse=True)
    return sum(splits[:top_n])


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve(3)}")

    test_results(solve(), solve(3))

