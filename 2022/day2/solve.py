from utils import parse_input, test_results

hands_map = {'A': 'rock', 'X': 'rock', 'B': 'paper', 'Y': 'paper', 'C': 'scissors', 'Z': 'scissors'}
winning_hands = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
loosing_hands = {v: k for k, v in winning_hands.items()}


def score(elf, me):
    """Calculate the round score based on chosen hands."""

    hand_score = {'rock': 1, 'paper': 2, 'scissors': 3}
    my_score = hand_score[me]
    if elf == me:
        my_score += 3
    elif (elf == 'rock' and me == 'paper') or (elf == 'paper' and me == 'scissors') \
            or (elf == 'scissors' and me == 'rock'):
        my_score += 6

    return my_score


def solve1():
    """Solve first part of the puzzle"""
    game_input = parse_input(convert_fn=lambda x: x.split())
    total_score = 0
    for line in game_input:
        elf, me = hands_map[line[0]], hands_map[line[1]]
        total_score += score(elf, me)

    return total_score


def solve2():
    """Solve second part of the puzzle"""
    game_input = parse_input(convert_fn=lambda x: x.split())
    total_score = 0
    for line in game_input:
        elf = hands_map[line[0]]
        strategy = line[1]
        if strategy == 'X': me = loosing_hands[elf]
        elif strategy == 'Y': me = elf
        elif strategy == 'Z': me = winning_hands[elf]
        total_score += score(elf, me)

    return total_score


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second  puzzle: {solve2()}")

    test_results(solve1(), solve2())
