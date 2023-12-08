from utils import parse_input


def get_cycles(commands):
    X = 1
    added = False
    cycles = []
    for c in commands:
        cycles.append(X)
        if added:
            cycles.append(X)
        if c[0] == 'addx':
            cycles.append(X)
            X += int(c[1])
    return cycles


def solve1():
    """Solve first part of the puzzle"""

    commands = parse_input(convert_fn=lambda s: s.split())
    key_cycles = [20, 60, 100, 140, 180, 220]
    cycles = get_cycles(commands)
    return sum([cycles[c-1] * c for c in key_cycles])


def solve2():
    """Solve second part of the puzzle"""

    commands = parse_input(convert_fn=lambda s: s.split())
    cycles = get_cycles(commands)

    i = 0
    for r in range(6):
        for c in range(40):
            if cycles[i] <= c+1 <= cycles[i]+2:
                print('■■■■', end='')
            else:
                print('    ', end='')
            i += 1
        print('\n')


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second  puzzle: \n")
    solve2()

