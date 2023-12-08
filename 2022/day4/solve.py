from utils import parse_input, l_to_i


def solve(min_matches=None):
    """Solve first part of the puzzle"""
    game_input = parse_input(convert_fn=lambda x: x.split(','))
    game_input = [(l_to_i(x[0].split('-')), l_to_i(x[1].split('-'))) for x in game_input]

    count = 0
    for x in game_input:
        set1 = set(range(x[0][0], x[0][1]+1))
        set2 = set(range(x[1][0], x[1][1]+1))
        n_matches = len(set1.intersection(set2))
        if n_matches in (len(set1), len(set2)) or (min_matches is not None and n_matches >= min_matches):
            count += 1

    return count


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve(1)}")
