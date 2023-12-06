from utils import input


def get_seeds_and_maps():
    """parse the input and create the mappings"""
    blocks = input(split_on='\n\n')
    seeds = list(map(int, blocks[0].split('seeds:')[1].split()))
    maps = []
    for block in blocks[1:]:
        map_lines = block.split('\n')
        range_map = []
        for range_line in map_lines[1:]:
            dest_start, source_start, length = map(int, range_line.split())
            range_map.append((dest_start, source_start, length))
        maps.append(range_map)

    return seeds, maps


def trace_seed(seed, maps):
    """Follow a seed down the tree"""

    next_seed = seed
    for m in maps:
        for range_i in m:
            dest_start, source_start, length = range_i
            if source_start <= next_seed < source_start + length:
                next_seed = dest_start + (next_seed - source_start)
                break
    return next_seed


def reverse_maps(maps):
    """Reverse the tree (top->bottom <--> bottom->top)"""
    return [[(source, dest, length) for dest, source, length in range_map] for range_map in maps[::-1]]


def check_seed(seed, seed_ranges):
    """Check if a seed is in the given seed ranges"""
    for seed_range in seed_ranges:
        if seed_range[0] <= seed <= seed_range[0] + seed_range[1]:
            return True
    return False


def solve():
    """Solve first part of the puzzle"""
    seeds, maps = get_seeds_and_maps()
    locations = []
    for seed in seeds:
        locations.append(trace_seed(seed, maps))
    return min(locations)


def solve2():
    """Solve second part of the puzzle"""

    seeds, maps = get_seeds_and_maps()
    seed_ranges = [(seeds[i], seeds[+1]) for i in range(0, len(seeds), 2)]
    seed_ranges = sorted(seed_ranges, key=lambda r: r[0])

    # do an inverse search (going from location to seeds)
    maps = reverse_maps(maps)

    max_loc = max([m[0]+m[2] for m in maps[0]])
    for i in range(max_loc):
        seed = trace_seed(i, maps)
        if check_seed(seed, seed_ranges):
            # found the lowest location which maps to a seed, so we can finish
            return i
    return None


if __name__ == "__main__":

   print(f"Solution to first puzzle: {solve()}")
   print(f"Solution to second  puzzle: {solve2()}")
