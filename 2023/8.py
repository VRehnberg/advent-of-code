import re
from itertools import cycle
from typing import IO, Iterable


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


class Loop:
    def __init__(self, initial_node, instructions, nodes):
        self.initial_node = initial_node
        location = self.initial_node
        loop_found = False
        visited: list[tuple(int, str)] = []
        for i_step, instruct in cycle(enumerate(instructions)):
            if (i_step, location) in visited:
                break
            location = nodes[location][instruct]
            visited.append((i_step, location))

        self.offset = i_step
        _, visited_nodes = zip(*visited)
        self.loop = tuple(visited_nodes[i_step:])

    def __len__(self):
        return len(self.loop)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.initial_node})"


def task2(instructions, nodes):
    # Find loops
    loops = [
        Loop(node, instructions, nodes)
        for node in nodes
        if node.endswith("A")
    ]
    print(loops)
    locations = [loop.initial_node for loop in loops]
    print(locations)

    # Check for stop before all loops have started
    offset = max(loop.offset for loop in loops)
    print(offset)
    print([len(loop) for loop in loops])
    for i_step, instruct in zip(range(offset), cycle(instructions)):
        if all(loc.endswith("Z") for loc in locations):
            print(i_step + 1)
            return
        locations = [nodes[loc][instruct] for loc in locations]

    print("TODO least_common_stop based on loops")
    # Possible offsets are loop.offset + [i for i, n in loop if n.endswith("Z")]
    # Check all LCM with offset for each


def main():
    with open("8.in") as f:
        instructions, nodes = parse(f)

    task1(instructions, nodes)
    task2(instructions, nodes)


if __name__ == "__main__":
    main()
