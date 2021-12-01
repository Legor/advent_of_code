from utils import input


def solve(k_size=3):
    """Solve first or second part of the puzzle"""
    r_in = input(convert_fn=int)
    sw_sum = [sum(r_in[i:i+k_size]) for i in range(len(r_in)-(k_size-1))]
    return len([True for i in range(1, len(sw_sum)) if sw_sum[i]-sw_sum[i-1] > 0])


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve(k_size=1)}")
    print(f"Solution to second  puzzle: {solve()}")
