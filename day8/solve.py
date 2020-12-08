from pathlib import Path


class Handheld:
    def __init__(self, instruction_file):
        self.accumulator = 0
        # parse to function eval format
        self.instructions = [(inst.split()[0], inst.split()[1]) for inst in Path(input_file).read_text().splitlines()]
        self.instruction_counter = [0] * len(self.instructions)
        self.index = 0

    def reset(self):
        self.instruction_counter = [0] * len(self.instructions)
        self.index = 0
        self.accumulator = 0

    def next(self):
        # program finished
        if self.index == len(self.instructions):
            return False
        elif self.index > len(self.instructions):
            raise RuntimeError(f'Invalid index at {self.index}')
        self.instruction_counter[self.index] += 1
        if self.instruction_counter[self.index] > 1:
            raise RuntimeError('Infinite loop')
        next_inst = self.instructions[self.index]
        eval(f'self.{next_inst[0]}({next_inst[1]})')
        return True

    def fix(self):
        for i in range(len(self.instructions)):
            orig_instruction = self.instructions[i]
            if orig_instruction[0] == 'nop':
                self.instructions[i] = ('jmp', orig_instruction[1])
            elif orig_instruction[0] == 'jmp':
                self.instructions[i] = ('nop', orig_instruction[1])
            try:
                self.run()
                return
            except RuntimeError as e:
                self.instructions[i] = orig_instruction
                continue

    def acc(self, value):
        self.accumulator += value
        self.index += 1

    def jmp(self, step):
        self.index += step

    def nop(self, value):
        self.index += 1

    def run(self):
        self.reset()
        keep_running = True
        while keep_running:
            keep_running = self.next()


def solve_first(input_file):
    handheld = Handheld(input_file)
    try:
        handheld.run()
    except RuntimeError as e:
        print(str(e) + f' --> Accumulator at {handheld.accumulator}')


def solve_second(input_file):
    handheld = Handheld(input_file)
    handheld.fix()
    try:
        handheld.run()
        print(f'Program finished --> Accumulator at {handheld.accumulator}')
    except RuntimeError as e:
        print(str(e) + f' --> Accumulator at {handheld.accumulator}')


if __name__ == "__main__":
    input_file = 'input.txt'
    print("Solution to first puzzle:")
    solve_first(input_file)
    print("Solution to second puzzle:")
    solve_second(input_file)