from utils import parse_input
from operator import add, sub, mul, truediv

ops = {'+': add, '-': sub, '*': mul, '/': truediv}


def solve_monkeys(monkeys):

    while True:
        solved = {m: v for m, v in monkeys.items() if type(v) == int}
        remaining = {m: v for m, v in monkeys.items() if m not in solved}
        for m, v in remaining.items():
            m1, op, m2 = v
            if m1 in solved and m2 in solved:
                monkeys[m] = int(ops[op](monkeys[m1], monkeys[m2]))
        if len(remaining) == 0:
            break

    return monkeys


def solve1():

    monkeys = parse_input(convert_fn=lambda x: x.split(': '))
    monkeys = {m[0]: int(m[1]) if m[1].isnumeric() else m[1].split() for m in monkeys}
    monkeys = solve_monkeys(monkeys)
    return monkeys['root']


def solve2():

    monkeys = parse_input(convert_fn=lambda x: x.split(': '))
    monkeys = {m[0]: int(m[1]) if m[1].isnumeric() else m[1].split() for m in monkeys}
    root = monkeys.pop('root')

    monkeys['humn'] = 1
    x_d = 1
    y0 = None
    while True:
        monkeys['humn'] += x_d
        monkeys_cp = solve_monkeys(monkeys.copy())
        y, v = int(monkeys_cp[root[0]]), int(monkeys_cp[root[2]])

        # initial run
        if y0 is None:
            y0 = y
        else:
            y_d = y-y0
            if y_d != 0:
                r_d = v-y
                x_d = max(int(r_d / (y_d / x_d)), 1)

        if int(monkeys_cp[root[0]]) == int(monkeys_cp[root[2]]):
            break

    return monkeys['humn']


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second puzzle: {solve2()}")
