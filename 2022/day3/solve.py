from utils import input


def score(letter):
    if letter.isupper():
        return ord(letter) - 38
    else:
        return ord(letter) - 96


def solve():
    """Solve first part of the puzzle"""

    game_input = input()
    game_input = [(x[:int(len(x)/2)], x[int(len(x)/2):]) for x in game_input]
    result = 0
    for t in game_input:
        for t1 in t[0]:
            if t1 in t[1]:
                result += score(t1)
                break
    return result


def solve2():
    """Solve second part of the puzzle"""

    game_input = input()
    result = 0
    for a, b, c in zip(*[iter(game_input)] * 3):
        for t in a:
            if t in b and t in c:
                result += score(t)
                break
    return result


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve2()}")
