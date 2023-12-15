from utils import parse_input
from collections import OrderedDict


def hashmap(instructions):
    boxes = [OrderedDict() for _ in range(256)]
    for ins in instructions:
        if '-' in ins:
            label = ins.split('-')[0]
            boxes[box_hash(label)].pop(label, None)
        elif '=' in ins:
            label, focal_length = ins.split('=')
            boxes[box_hash(label)][label] = int(focal_length)
    return boxes


def focussing_power(boxes):
    return sum((1 + i) * (j + 1) * val for i, box in enumerate(boxes) for j, val in enumerate(box.values()))


def box_hash(s):
    result = 0
    for c in s:
        result = (result + ord(c)) * 17 % 256
    return result


if __name__ == "__main__":

    instructions = parse_input(split_on=',')
    print(f"Solution to first puzzle: {sum([box_hash(tok) for tok in instructions])}"),
    print(f"Solution to second puzzle: {focussing_power(hashmap(instructions))}")
