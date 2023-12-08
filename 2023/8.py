import re
from itertools import cycle, count
from typing import IO, Iterable
from math import lcm

import numpy as np
from tqdm import tqdm


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

    return i_step


class Loop:
    def __init__(self, initial_node, instructions, nodes):
        self.initial_node = initial_node
        location = self.initial_node
        loop_found = False
        visited: dict[tuple(int, str), None] = {}  # ordered set
        for i_instruct, instruct in cycle(enumerate(instructions)):
            step_id = (i_instruct, location)
            if step_id in visited:
                break
            visited[step_id] = None
            location = nodes[location][instruct]

        assert any(node.endswith("Z") for _, node in visited)

        i_loop_start = list(visited.keys()).index(step_id)
        _, visited_nodes = zip(*visited)
        self._nodes_before_loop = tuple(visited_nodes[:i_loop_start])
        self.loop = tuple(visited_nodes[i_loop_start:])
        self.offset = len(self._nodes_before_loop)

    def __len__(self):
        return len(self.loop)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.initial_node})"

    @property
    def stops(self):
        #print(self._nodes_before_loop)
        yield from (
            i_step
            for i_step, node in enumerate(self._nodes_before_loop)
            if node.endswith("Z")
        )
        stops_in_loop = [
            i_in_loop
            for i_in_loop, node in enumerate(self.loop)
            if node.endswith("Z")
        ]
        assert len(stops_in_loop) == 1
        #print(self.loop)
        #print(stops_in_loop)
        assert len(stops_in_loop) >= 1
        print(self, stops_in_loop, [self.loop[i] for i in stops_in_loop], self.offset)
        for i_loop in count(start=0, step=1):
            offset = self.offset + i_loop * len(self)
            for stop in stops_in_loop:
                yield stop + offset


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

    for loop in loops:
        print(loop, f"{len(loop)} N + {next(iter(loop.stops))}")

        assert len(loop) == next(iter(loop.stops))

    return lcm(*(len(loop) for loop in loops))
    ## Loop over stops in loops
    #stop_iters = [iter(loop.stops) for loop in loops]
    #current_stops = np.array([next(stop_iter) for stop_iter in stop_iters])
    #print(current_stops)
    #all_stop = np.all(current_stops == current_stops[-1])
    #while not all_stop:
    #    for i_loop, stop_iter in enumerate(stop_iters):
    #        if np.any(current_stops[i_loop] < current_stops):
    #            current_stops[i_loop] = next(stop_iter)
    #    all_stop = np.all(current_stops == current_stops[-1])

    #assert np.all(current_stops == current_stops[0])
    #return current_stops[0]


def main():
    with open("8.in") as f:
        instructions, nodes = parse(f)

    #print(task1(instructions, nodes))
    print(task2(instructions, nodes))


if __name__ == "__main__":
    main()
