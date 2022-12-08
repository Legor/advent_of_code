from utils import grid, get_mask, prod


def is_visible(tree_map, r_i, c_i):

    h = tree_map[r_i][c_i]
    if (max(tree_map[r_i][:c_i]) < h) or (max(tree_map[r_i][c_i+1:]) < h) \
            or (max([r[c_i] for r in tree_map[:r_i]]) < h) or (max([r[c_i] for r in tree_map[r_i+1:]]) < h):
            # ↑ need to slice columns differently (would be easier with numpy) ↑
        return True
    return False


def scenic_score(tree_mask, r_i, c_i):
    """Compute the scenic score for the given tree at index (r_i, c_i) with the given tree mask."""

    row = tree_mask[r_i]
    # need to slice columns differently (would be easier with numpy)
    col = [r[c_i] for r in tree_mask]
    # sub arrays (excluding the reference element). Invert the left/up arrays for easier counting
    # left, right, up, down
    splits = row[:c_i][::-1], row[c_i+1:], col[:r_i][::-1], col[r_i+1:]
    score = []
    for sp in splits:
        try:
            # This is the first occurrence of a tree equal or larger than the current tree
            # index gives array index, but we need the number for the score
            score.append(sp.index(True)+1)
        except ValueError:
            # if no such tree exists, use the count until the end of the map (equal to the sub array length)
            score.append(len(sp))
    # the scenic score is the product of all direction scores
    return prod(score)


def solve1():
    """Solve first part of the puzzle"""

    tree_map = grid()
    shape = (len(tree_map), len(tree_map[0]))

    # the border trees are all visible
    count = 2 * (shape[0] + shape[1] - 2)
    for r_i in range(1, shape[0]-1):
        for c_i in range(1, shape[1]-1):
            if is_visible(tree_map, r_i, c_i):
                count += 1

    return count


def solve2():
    """Solve second part of the puzzle"""

    tree_map = grid()
    shape = (len(tree_map), len(tree_map[0]))
    # init tree masks (for faster runtime)
    # contains, for each tree size (0-9), where on the map a tree is equal or larger than this size
    tree_masks = [get_mask(tree_map, cond=lambda v: v >= i) for i in range(0, 10)]
    scores = []
    # for each tree (excluding border trees)
    for r_i in range(1, shape[0]-1):
        for c_i in range(1, shape[1]-1):
            # use the tree mask for the current tree size
            tree_sz = tree_map[r_i][c_i]
            scores.append(scenic_score(tree_masks[tree_sz], r_i, c_i))

    return max(scores)


if __name__ == "__main__":

    print(f"Solution to first puzzle: {solve1()}")
    print(f"Solution to second  puzzle: {solve2()}")
