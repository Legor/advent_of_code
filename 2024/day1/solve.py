from utils import parse_input

def solve(left, right):
    """Solve first part of the puzzle"""
    return sum([abs(le-r) for le, r in zip(left, right)])

def solve2(left, right):
    """Solve second part of the puzzle"""
    return sum([right.count(le) * le for le in left])

if __name__ == "__main__":

    # parse lists
    left, right = map(lambda l: sorted(l), zip(*parse_input(convert_fn=lambda l: list(map(int, str.split(l))))))
    print(f"Solution to first puzzle: {solve(left, right)}")
    print(f"Solution to second  puzzle: {solve2(left, right)}")
