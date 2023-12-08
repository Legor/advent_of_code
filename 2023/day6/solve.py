from utils import parse_input
import math


def quadratic_equation(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None  # No real roots if the discriminant is negative
    else:
        root1 = (-b - discriminant ** 0.5) / (2 * a)
        root2 = (-b + discriminant ** 0.5) / (2 * a)
        return root1, root2


def solve(times, distances):
    """Solve first or second part of the puzzle"""

    times, distances = list(map(int, times)), list(map(int, distances))
    total_wins = 1
    for t, d in zip(times, distances):
        x1, x2 = quadratic_equation(1, -1*t, d+1)
        x1, x2 = math.ceil(x1), math.floor(x2)
        total_wins *= x2-x1+1
    return total_wins


if __name__ == "__main__":

    times, distances = parse_input(convert_fn=lambda s: s.split()[1:])
    print(f"Solution to first puzzle: {solve(times, distances)}")
    print(f"Solution to second  puzzle: {solve([''.join(times)], [''.join(distances)])}")
