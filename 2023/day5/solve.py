from utils import input
from functools import cache, lru_cache
from tqdm.auto import tqdm


def solve():
    """Solve first part of the puzzle"""
    lines = input(split_on='\n\n')
    seeds = map(int, lines[0].split('seeds:')[1].split())
    maps = []
    for m in lines[1:]:
        map_lines = m.split('\n')
        range_map = []
        for range_line in map_lines[1:]:
            dest_start, source_start, length = map(int, range_line.split())
            #range_map.update({source_start+i: dest_start+i for i in range(length)})
            range_map.append((dest_start, source_start, length))
        #maps[map_lines[0]] = range_map
        maps.append(range_map)

    locations = []
    for seed in seeds:
        print('___')
        next_seed = seed
        for m in maps:
            print('M', m)
            print(next_seed)
            found = False
            for range_i in m:
                dest_start, source_start, length = range_i
                if source_start <= next_seed < source_start+length:
                    next_seed = dest_start + (next_seed - source_start)
                    break

            #next_seed = m[next_seed]
        locations.append(next_seed)

    return min(locations)


seed_map = []

@lru_cache(maxsize=None)
def get_location(seed):
    #next_seed = seed
    #for range_map in seed_map:
    #    next_seed = get_next_seed(range_map, next_seed)
    return get_next_seed(0, seed)


#@lru_cache(maxsize=10024)
#def get_next_seed(range_map, seed):
    #for range_i in range_map:
    #    dest_start, source_start, length = range_i
    #    if source_start <= seed < source_start + length:
    #        return dest_start + (seed - source_start)
    #return seed




@lru_cache(maxsize=None)
def get_next_seed(i, seed):
    next_seed = seed
    for range_i in seed_map[i]:
        dest_start, source_start, length = range_i
        if source_start <= seed < source_start + length:

            next_seed = dest_start + (seed - source_start)
            break

    if i == len(seed_map)-1:
        return next_seed
    #print(i, seed, next_seed)
    return get_next_seed(i+1, next_seed)


def solve2():
    """Solve first part of the puzzle"""
    lines = input(split_on='\n\n')
    seeds = list(map(int, lines[0].split('seeds:')[1].split()))
    seed_ranges = [(seeds[i], seeds[+1]) for i in range(0, len(seeds), 2)]
    global seed_map
    for m in lines[1:]:
        map_lines = m.split('\n')
        range_map = []
        for range_line in map_lines[1:]:
            dest_start, source_start, length = map(int, range_line.split())
            range_map.append(tuple([dest_start, source_start, length]))
        seed_map.append(tuple(range_map))

    seed_map = tuple(seed_map)
    locations = []
    solved = {}
    for seed_range in seed_ranges:
        for seed in tqdm(range(seed_range[0], seed_range[0]+seed_range[1])):
            #print('Start ', seed)
            next_seed = get_next_seed(0, seed)
            info = get_next_seed.cache_info()
            if info.hits != 0:
                print(info)

            #next_seed = seed
            #if next_seed not in solved:
            #    for i_m, m in enumerate(maps):
            #        for range_i in m:
            #            dest_start, source_start, length = range_i
            #            if source_start <= next_seed < source_start+length:
            #                next_seed = dest_start + (next_seed - source_start)
            #                break

                #solved[seed] = next_seed

            locations.append(next_seed)

    return min(locations)




if __name__ == "__main__":

    #print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second  puzzle: {solve2()}")
