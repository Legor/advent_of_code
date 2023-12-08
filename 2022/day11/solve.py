from utils import parse_input, prod


class Monkey:

    def __init__(self, monkey_str: str, worry_divisor=1):

        s = monkey_str.splitlines()
        self.items = [int(t.strip(',')) for t in s[1].split()[2:]]
        # hack to store expression as member, using exec
        self.op = {}
        op_str = s[2].split(': ')[1].replace('=', '= lambda old:')
        exec(op_str, globals(), self.op)

        self.test_val = int(s[3].split()[-1])
        self.test_res = {True: int(s[4].split()[-1]), False: int(s[5].split()[-1])}
        self.inspections = 0
        self.worry_divisor = worry_divisor

    def test(self, val):
        return self.test_res[(val % self.test_val) == 0]

    def inspect(self):
        self.items = [int((self.op['new'](item)) / self.worry_divisor) for item in self.items]
        self.inspections += len(self.items)


def solve(n_rounds, worry_divisor):

    raw_input = parse_input(split_on='\n\n')
    monkeys = []
    for s in raw_input:
        monkeys.append(Monkey(s, worry_divisor))

    mod_prod = prod([m.test_val for m in monkeys])

    for n in range(n_rounds):
        for i, m in enumerate(monkeys):
            m.inspect()
            for item in m.items:
                # give item to next monkey
                target = m.test(item)
                monkeys[target].items.append(item % mod_prod)

            m.items = []

    monkeys = sorted(monkeys, key=lambda m: m.inspections, reverse=True)
    return monkeys[0].inspections * monkeys[1].inspections


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve(n_rounds=20, worry_divisor=3)}")
    print(f"Solution to second puzzle: {solve(n_rounds=10000, worry_divisor=1)}")
