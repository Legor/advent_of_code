from pathlib import Path
import re


def parse_rules(input_file):
    """Build the rule tree"""
    raw_input = Path(input_file).read_text().splitlines()
    matcher = re.compile('.*(\d+) (\S+ \S+)')
    bag_rules = {}
    for line in raw_input:
        toks = line.split('contain')
        bag = "_".join(toks[0].split()[:2])
        content = []
        for c in toks[1].split(','):
            m = matcher.match(c)
            if m:
                content.append((m.groups()[1].replace(' ', '_'), int(m.groups()[0])))
        bag_rules[bag] = content
    return bag_rules


def count_bags(bag_rules, bag_id, searched_bag=None):
    if len(bag_rules[bag_id]) == 0:
        return 0
    # count only a specific bag type
    if searched_bag:
        return sum([x[1] if x[0] == searched_bag else count_bags(bag_rules, x[0], searched_bag)
                    for x in bag_rules[bag_id]])
    # count all bags
    else:
        return sum([x[1] + x[1] * count_bags(bag_rules, x[0]) for x in bag_rules[bag_id]])


def solve_first(input_file):
    """Count in how many bags a shiny gold bag is allowed."""
    bag_rules = parse_rules(input_file)
    count = 0
    for bag_id in bag_rules.keys():
        if count_bags(bag_rules, bag_id, 'shiny_gold'):
            count += 1
    return count


def solve_second(input_file):
    """Count how many bags are contained in a shiny gold bag."""
    bag_rules = parse_rules(input_file)
    return count_bags(bag_rules, 'shiny_gold')


if __name__ == "__main__":
    input_file = 'input.txt'
    print(f"Solution to first puzzle: {solve_first(input_file)}")
    print(f"Solution to second  puzzle: {solve_second(input_file)}")