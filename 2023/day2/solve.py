from utils import parse_input, prod
import re

MAX_CUBES = {'red': 12, 'green': 13, 'blue': 14}
color_pattern = r'(\d+) (red|green|blue)'


def parse():
    game_pattern = r'Game (\d+): (.*)'
    games = parse_input(convert_fn=lambda line: re.match(game_pattern, line))
    return {int(game.group(1)): game.group(2).split(';') for game in games}


def solve():
    """Solve first part of the puzzle"""

    games = parse()
    impossible_games = []
    for game_id, game in games.items():
        for draw in game:
            for cube in re.findall(color_pattern, draw):
                number, color = cube
                if int(number) > MAX_CUBES[color]:
                    impossible_games.append(game_id)

    return sum(set(impossible_games) ^ set(games))


def solve2():
    """Solve second part of the puzzle"""
    games = parse()

    total_sum = 0
    for game_id, game in games.items():
        max_colors = {'red': 0, 'green': 0, 'blue': 0}
        for draw in game:
            for cube in re.findall(color_pattern, draw):
                number, color = cube
                if int(number) > max_colors[color]:
                    max_colors[color] = int(number)

        total_sum += prod(max_colors.values())
    return total_sum


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve2()}")
