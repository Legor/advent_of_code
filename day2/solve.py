from pathlib import Path
import re


def solve_first(input_file):
    """Solve first part of the puzzle"""
    raw_input = Path('./input.txt').read_text().splitlines()
    pattern = re.compile('(?P<min>\d+)-(?P<max>\d+) (?P<letter>\S): (?P<pwd>\S+)')
    pwd_list = [pattern.match(line) for line in raw_input]
    valid_count = 0
    for entry in pwd_list:
        letter_count = entry['pwd'].count(entry['letter'])
        if letter_count >= int(entry['min']) and letter_count <= int(entry['max']):
            valid_count += 1

    return valid_count


def solve_second(input_file):
    """Solve second part of the puzzle"""
    raw_input = Path('./input.txt').read_text().splitlines()
    pattern = re.compile('(?P<first_pos>\d+)-(?P<second_pos>\d+) (?P<letter>\S): (?P<pwd>\S+)')
    pwd_list = [pattern.match(line) for line in raw_input]
    valid_count = 0
    for entry in pwd_list:
        letter_count = entry['pwd'].count(entry['letter'])
        if letter_count > 0:
            # take care of 1-based indexing
            letter_positions = [match.start()+1 for match in re.finditer(entry['letter'],  entry['pwd'])]
            if ((int(entry['first_pos']) in letter_positions and not int(entry['second_pos']) in letter_positions) or
                    (int(entry['second_pos']) in letter_positions and not int(entry['first_pos']) in letter_positions)):
                valid_count += 1

    return valid_count


if __name__ == "__main__":

    input_file = 'input.txt'
    print(f"Solution of first puzzle: {solve_first(input_file)}")
    print(f"Solution of second  puzzle: {solve_second(input_file)}")
