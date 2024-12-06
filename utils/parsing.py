from pathlib import Path


def parse_input(file="input.txt", split_on="\n", convert_fn=None):
    lines = Path(file).read_text()
    if split_on:
        lines = lines.split(split_on)
    if convert_fn:
        lines = [convert_fn(x) for x in lines]
    return lines
