from utils import parse_input


def solve():
    """Solve first part of the puzzle"""
    lines = parse_input(convert_fn=lambda s: s.split('|'))
    guesses = [line[0].split(':')[1].split() for line in lines]
    winning_numbers = [line[1].split() for line in lines]

    hits = [len(set(g) & set(w)) for g, w in zip(guesses, winning_numbers)]
    return sum([2 ** (h-1) for h in hits if h > 0])


n_cards = 0
def scratch(cards, c_i):
    global n_cards
    n_cards += 1

    if cards[c_i] == 0:
        return

    for i in range(1, cards[c_i]+1):
        scratch(cards, c_i+i)


def solve2():
    """Solve second part of the puzzle"""
    lines = parse_input(convert_fn=lambda s: s.split('|'))
    guesses = [line[0].split(':')[1].split() for line in lines]
    winning_numbers = [line[1].split() for line in lines]

    cards = [len(set(g) & set(w)) for g, w in zip(guesses, winning_numbers)]

    for i in range(len(cards)):
        scratch(cards, i)

    return n_cards


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve2()}")
