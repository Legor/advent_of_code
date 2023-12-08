from utils import parse_input, get_nb_indices, find_pattern_in_lines


def solve():
    """Solve first part of the puzzle"""
    lines = parse_input()
    # find all numbers per row
    numbers = find_pattern_in_lines(lines, r'\d+')
    # find all special symbols per row (none digit and none '.')
    symbols = find_pattern_in_lines(lines, r'[^.\d]')
    # the 2d-indices of each special symbol
    symbol_indices = [(row, m.start()) for row, row_matches in enumerate(symbols) for m in row_matches]

    total_sum = 0
    for y, row_numbers in enumerate(numbers):
        for number in row_numbers:
            # look at the neighborhood of each digit for this number
            for x in range(number.start(), number.end()):
                nb_indices = get_nb_indices(y, x)
                # if at least one neighbor contains a special symbol, add the number
                if len([idx for idx in nb_indices if idx in symbol_indices]) > 0:
                    total_sum += int(number.group())
                    break

    return total_sum


def solve2():
    """Solve first part of the puzzle"""
    lines = parse_input()
    # find all numbers per row
    numbers = find_pattern_in_lines(lines, r'\d+')
    # find all special symbols per row (none digit and none '.')
    gears = find_pattern_in_lines(lines, r'[*]')
    # the 2d-indices of each special symbol
    gears_indices = [(row, m.start()) for row, row_matches in enumerate(gears) for m in row_matches]

    total_sum = 0
    for idx in gears_indices:
        # get neighbor indices
        nb_idx = get_nb_indices(idx[0], idx[1])
        hits = []
        for y, match in enumerate(numbers):
            for number in match:
                if (y, number.start()) in nb_idx or (y, number.end()-1) in nb_idx:
                    hits.append(number)
        if len(hits) == 2:
            total_sum += int(hits[0].group()) * int(hits[1].group())

    return total_sum


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve2()}")
