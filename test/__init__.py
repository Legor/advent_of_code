from pathlib import Path
from utils import parse_input

def test_results(solve1, solve2, file='solutions.txt'):
    if Path(file).exists():
        solutions = parse_input(file, convert_fn=int)
        print('\u2705' if solve1 == solutions[0] else '\u274C ', f' {solve1} == {solutions[0]}')
        print('\u2705' if solve2 == solutions[1] else '\u274C ', f' {solve2} == {solutions[1]}')
    else:
        print('Skipping test, no solutions found.')