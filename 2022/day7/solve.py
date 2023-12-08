from utils import parse_input
from pathlib import Path


def build_dir_tree(game_input):

    cd = Path('/')
    dirs = {cd: []}

    # controls if previous listing
    ls = False
    for line in game_input:
        parts = line.split()

        if parts[0] == '$':
            if parts[1] == 'cd':
                ls = False
                if parts[2] == '..':
                    cd = cd.parent
                else:
                    cd = cd.joinpath(parts[2])
                assert cd in dirs

            elif parts[1] == 'ls':
                ls = True

        elif ls:
            # add new path as listed
            if parts[0] == 'dir':
                subdir = cd.joinpath(parts[1])
                if subdir not in dirs:
                    dirs[subdir] = []
            # expect a file
            else:
                assert parts[0].isnumeric(), f'Expected a file listing, {parts}'
                dirs[cd].append((int(parts[0]), parts[1]))

    return dirs


def calc_sizes(dir_tree):
    """Calculate the size of each directory."""

    def get_subdirs(parent_dir):
        return [sub_d for sub_d in dir_tree if parent_dir in sub_d.parents]

    flat_sizes = {d: sum([f[0] for f in files]) for d, files in dir_tree.items()}
    total_sizes = {d: 0 for d in dir_tree}
    for d in dir_tree:
        # add current dirs own flat size
        total_sizes[d] += flat_sizes[d]
        # iterate each subdir for the current dir
        for sub_d in get_subdirs(d):
            # list of files for this subdir
            total_sizes[d] += flat_sizes[sub_d]

    return total_sizes


def solve1(max_size=100000):
    """Solve first part of the puzzle"""

    game_input = parse_input()
    dirs = build_dir_tree(game_input)
    dir_sizes = calc_sizes(dirs)
    return sum([sz for sz in dir_sizes.values() if sz <= max_size])


def solve2(disk_space=70000000, update_size=30000000):
    """Solve second part of the puzzle"""

    game_input = parse_input()
    dirs = build_dir_tree(game_input)
    dir_sizes = calc_sizes(dirs)

    free = disk_space - dir_sizes[Path('/')]
    needed = update_size - free
    return min([sz for sz in dir_sizes.values() if sz >= needed])


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second  puzzle: {solve2()}")
