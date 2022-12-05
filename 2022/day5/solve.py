from utils import input, chunks, l_to_i


def parse_crates(crates_str):

    lines = crates_str.splitlines()
    n_staples = max(map(int, lines[-1].split()))
    crates = [[] for i in range(n_staples)]
    for line in lines[:-1]:
        tmp_chunks = [c.strip(' []') for c in chunks(line, 4)]
        for i, entry in enumerate(tmp_chunks):
            if len(entry) > 0:
                crates[i].insert(0, entry)
    return crates


def parse_commands(commands_str):

    commands = []
    for line in commands_str.splitlines():
        toks = line.split()
        commands.append(l_to_i([toks[1], toks[3], toks[5]]))
    return commands


def solve(keep_order=False):
    """Solve first part of the puzzle"""
    game_input = input(split=False)
    game_input = game_input.split('\n\n')

    crates = parse_crates(game_input[0])
    commands = parse_commands(game_input[1])

    for command in commands:
        mv_from = command[1] - 1
        mv_to = command[2] - 1
        crate_mv = []
        for mv in range(command[0]):
            if keep_order:
                crate_mv.insert(0, crates[mv_from].pop())
            else:
                crate_mv.append(crates[mv_from].pop())

        crates[mv_to] = crates[mv_to] + crate_mv
    return "".join([c[-1] for c in crates])


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve(keep_order=True)}")
