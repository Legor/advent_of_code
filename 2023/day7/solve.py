from utils import input
from collections import Counter
import functools
import itertools

CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
# map counts of unique cards to value
HAND_VALUES = {(5,): 6, (4, 1): 5, (3, 2): 4, (3, 1, 1): 3, (2, 2, 1): 2, (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}


def replace_chars(s, chars, positions):
    s_list = list(s)
    for char, pos in zip(chars, positions):
        s_list[pos] = char
    return ''.join(s_list)


def hand_value(hand, use_joker=False):
    counts = Counter(hand)

    if use_joker and 'J' in counts:
        if len(counts) == 1:
            return hand_value(hand.replace('J', 'A'))
        elif len(counts) == 2:
            return hand_value(hand.replace('J', hand.replace('J', '')[0]))

        joker_i = [i for i, c in enumerate(hand) if c == 'J']
        all_combinations = itertools.product(CARD_VALUES, repeat=len(joker_i))
        permutations = [replace_chars(hand, combo, joker_i) for combo in all_combinations]
        permutations = sorted(permutations, key=functools.cmp_to_key(sort_hands))
        return hand_value(permutations[-1])

    card_counts = sorted(counts.values(), reverse=True)
    return HAND_VALUES[tuple(card_counts)]


def sort_hands(hand1, hand2, use_joker=False):
    hand_value1, hand_value2 = hand_value(hand1, use_joker), hand_value(hand2, use_joker)
    # break ties
    if hand_value1 == hand_value2:
        # get the card values of the first card pair that is not equal
        hand_value1, hand_value2 = [CARD_VALUES.index(card) for card in
                                    [(card1, card2) for card1, card2 in zip(hand1, hand2) if card1 != card2][0]]
    return 1 if hand_value1 > hand_value2 else -1


if __name__ == "__main__":

    game = input(convert_fn=lambda s: s.split())
    hands = [g[0] for g in game]
    bets = [g[1] for g in game]

    ranked = sorted(zip(hands, bets),
                    key=functools.cmp_to_key(lambda hand1, hand2: sort_hands(hand1[0], hand2[0])))
    result = sum([int(r[1]) * i for i, r in enumerate(ranked, start=1)])
    print(f"Solution to first puzzle: {result}")

    CARD_VALUES.remove('J')
    CARD_VALUES.insert(0, 'J')
    ranked = sorted(zip(hands, bets),
                    key=functools.cmp_to_key(lambda hand1, hand2: sort_hands(hand1[0], hand2[0], True)))
    result = sum([int(r[1]) * i for i, r in enumerate(ranked, start=1)])
    print(f"Solution to second  puzzle: {result}")
