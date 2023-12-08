import re
from itertools import cycle
from typing import IO


re_nodes = re.compile(r"^([0-9A-Z]+) = [(]([0-9A-Z]+), ([0-9A-Z]+)[)]$")


def parse(file: IO) -> tuple[str, dict[str, tuple[str, str]]]:
        instruct2index = {
            "L": 0,
            "R": 1,
        }
        instructions = [instruct2index[instruct] for instruct in next(file).strip()]
        assert next(file).strip() == ""

        nodes: dict[str, tuple[str, str]] = {}
        for line in file:
            match = re_nodes.match(line.strip())
            nodes[match.group(1)] = (match.group(2), match.group(3))

        return instructions, nodes


def task1(instructions, nodes):
    location = "AAA"
    for i_step, instruct in enumerate(cycle(instructions)):
        if location == "ZZZ":
            break
        location = nodes[location][instruct]

    print(i_step)


def task2(instructions, nodes):
    locations = [node for node in nodes if node.endswith("A")]
    print(locations)
    for i_step, instruct in enumerate(cycle(instructions)):
        if all(loc.endswith("Z") for loc in locations):
            break
        locations = [nodes[loc][instruct] for loc in locations]
        #assert not any((loc, loc) == nodes[loc] for loc in locations), "Stuck"
    print(i_step)


def main():
    with open("8.in") as f:
        instructions, nodes = parse(f)

    task1(instructions, nodes)
    task2(instructions, nodes)


if __name__ == "__main__":
    main()
