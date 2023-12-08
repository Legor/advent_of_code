from utils import parse_input
import functools


def compare(left, right):

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return -1
        else:
            return left < right
    if isinstance(left, list) and isinstance(right, list):
        for i in range(len(right)):
            if i < len(left):
                comp = compare(left[i], right[i])
                if comp == -1:
                    continue
                return comp
            else:
                return True
        if len(right) < len(left):
            return False
        else:
            return -1
    if isinstance(left, int):
        return compare([left], right)
    else:
        return compare(left, [right])


def sort_fn(left, right):
    if compare(left, right):
        return -1
    else:
        return 1


def solve1():

    # pad grid for easier processing
    signals = parse_input(split_on='\n\n', convert_fn=lambda s: s.splitlines())
    sum = 0
    for i, sig in enumerate(signals):
        left = eval(sig[0])
        right = eval(sig[1])
        if compare(left, right):
            sum += i+1
    return sum


def solve2():

    # pad grid for easier processing
    signals = parse_input()
    signals += ['[[2]]', '[[6]]']
    signals = [eval(s) for s in signals if len(s) > 0]
    sort_sig = sorted(signals, key=functools.cmp_to_key(sort_fn))
    return (sort_sig.index([[2]])+1) * (sort_sig.index([[6]])+1)


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second puzzle: {solve2()}")
