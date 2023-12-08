from utils import parse_input


def solve(encryption_key=1, n_mix=1):

    numbers = parse_input(convert_fn=lambda x: int(x) * encryption_key)
    indices = list(range(len(numbers)))
    N = len(numbers)

    for m in range(n_mix):
        for i in range(N):
            val = numbers[i]
            idx = indices.index(i)
            new_idx = (idx + val) % (N - 1)
            indices.pop(idx)
            indices.insert(new_idx, i)

    numbers = [numbers[j] for j in indices]
    idx = numbers.index(0)
    keys = (1000, 2000, 3000)
    return sum([numbers[(((i + idx % N) + N) % N)] for i in keys])


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve()}")
    print(f"Solution to second puzzle: {solve(encryption_key=811589153, n_mix=10)}")
