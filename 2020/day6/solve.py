from pathlib import Path


def parse_groups(input_file):
    raw_input = Path(input_file).read_text().splitlines()
    groups = [[]]
    for line in raw_input:
        if len(line) == 0:
            groups.append([])
        else:
            groups[-1].append(line)
    return groups


def solve_first(input_file):
    groups = parse_groups(input_file)
    # count distinct answers per group
    return sum([len(set(''.join(g))) for g in groups])


def solve_second(input_file):
    groups = parse_groups(input_file)
    # get distinct answers per group
    uniques = [set(''.join(g)) for g in groups]

    count = 0
    for g, u in zip(groups, uniques):
        # special case, only one answer given or only 1 person in group
        if len(g) == 1 or len(u) == 1:
            count += len(u)
        else:
            count += sum([sum([x in y for y in g]) == len(g) for x in u])
    return count


if __name__ == "__main__":
    input_file = 'input.txt'
    print(f"Solution to first puzzle: {solve_first(input_file)}")
    print(f"Solution to second puzzle: {solve_second(input_file)}")
