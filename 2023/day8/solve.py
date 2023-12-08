from utils import parse_input, BinaryTree, TreeNode, find_lcm
import re


def follow_instructions(start_leaf: 'TreeNode', end_leafs: list, instructions: str):
    """From a start leaf follow the instructions until one of end_leafs is found. Returns the number of steps needed."""

    steps = 0
    while True:
        if instructions[steps % len(instructions)] == 'L':
            start_leaf = start_leaf.left
        else:
            start_leaf = start_leaf.right

        steps += 1
        if start_leaf in end_leafs:
            break
    return steps


def solve(bt, instructions):
    """Solve first part of the puzzle"""
    return follow_instructions(bt['AAA'], [bt['ZZZ']], instructions)


def solve2(bt, instructions):
    """Solve first part of the puzzle"""

    starting_leafs = [leaf for value, leaf in bt.leafs.items() if value.endswith('A')]
    end_leafs = [leaf for value, leaf in bt.leafs.items() if value.endswith('Z')]
    steps = [follow_instructions(start_leaf, end_leafs, instructions) for start_leaf in starting_leafs]
    return find_lcm(steps)


if __name__ == "__main__":

    # build tree
    instructions, nodes = parse_input(split_on='\n\n')
    instructions, nodes = instructions.splitlines()[0], nodes.splitlines()
    bt = BinaryTree()
    for node in nodes:
        node, leafes = node.split(' = ')
        leafes = re.sub(r'[()\s]', '', leafes).split(',')
        bt.add_leaf(node, leafes)

    print(f"Solution to first puzzle: {solve(bt, instructions)}")
    print(f"Solution to second  puzzle: {solve2(bt, instructions)}")
