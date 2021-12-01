from pathlib import Path
import re


class Ferry:

    def __init__(self, instruction_file='input.txt'):
        self.instructions = Path(instruction_file).read_text().splitlines()
        self.instructions = [re.match('(\D)(\d+)', s).groups() for s in self.instructions]
        self.movement = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (0, -1)}
        self.facing = 'E'
        self.position = {'x': 0, 'y': 0}

    def move(self, direction, distance):
        if direction == 'F':
            direction = self.facing
        self.position['x'] += self.movement[direction][0] * distance
        self.position['y'] += self.movement[direction][1] * distance

    def turn(self, direction, value):
        rose = ('N', 'E', 'S', 'W')
        turn = -1 if direction == 'L' else 1
        turn *= int(value / 45)
        turn = rose.index(self.facing) + turn
        turn = turn % 4
        self.facing = rose[turn]

    def start_engine(self):
        for instr in self.instructions:
            if instr[0] in ['N', 'E', 'S', 'W', 'F']:
                self.move(instr[0], int(instr[1]))
            elif instr[0] in ['L', 'R']:
                self.turn(instr[0], int(instr[1]))

def solve_first():
    ferry = Ferry()
    ferry.start_engine()
    return sum([abs(x) for x in ferry.position.values()])

if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve_first()}")
    #print(f"Solution to second  puzzle: {solve_second()}")