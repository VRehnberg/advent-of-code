from collections import Counter, deque
from dataclasses import dataclass
from itertools import count
from typing import IO

import numpy as np
import numpy.typing


@dataclass(kw_only=True)
class Tile:
    north: bool
    south: bool
    west: bool
    east: bool
    is_start: bool = False

    def __post_init__(self):
        n_connections = (
            int(self.north)
            + int(self.south)
            + int(self.west)
            + int(self.east)
        )
        assert n_connections == 2 or n_connections == 0

    @classmethod
    def from_str(cls, tile: str):
        assert isinstance(tile, str) and len(tile) == 1
        if tile == "|":
            return cls(
                north=True,
                south=True,
                west=False,
                east=False,
            )
        elif tile == "-":
            return cls(
                north=False,
                south=False,
                west=True,
                east=True,
            )
        elif tile == "L":
            return cls(
                north=True,
                south=False,
                west=False,
                east=True,
            )
        elif tile == "J":
            return cls(
                north=True,
                south=False,
                west=True,
                east=False,
            )
        elif tile == "7":
            return cls(
                north=False,
                south=True,
                west=True,
                east=False,
            )
        elif tile == "F":
            return cls(
                north=False,
                south=True,
                west=True,
                east=False,
            )
        elif tile == ".":
            return cls(
                north=False,
                south=False,
                west=False,
                east=False,
            )
        elif tile == "S":
            return cls(
                is_start=True,
                north=False,
                south=False,
                west=False,
                east=False,
            )
        else:
            ValueError(f"Tile {tile} not recognized")

    def __repr__(self):
        if self.is_start:
            return "S"
        if self.north:
            if self.south:
                return "|"
            if self.east:
                return "L"
            if self.west:
                return "J"
        if self.south:
            if self.east:
                return "F"
            if self.west:
                return "7"
        if self.west and self.east:
            return "-"
        return "."


def parse(file: IO) -> np.typing.NDArray[Tile]:
    grid = np.array([
        [Tile.from_str(c) for c in line.strip()]
        for line in file
    ])
    i, j = np.where(grid == Tile.from_str("S"))
    i, j = i.item(), j.item()
    grid[i, j].north = grid[i - 1, j].south
    grid[i, j].south = grid[i + 1, j].north
    grid[i, j].west = grid[i, j - 1].east
    grid[i, j].east = grid[i, j + 1].west
    return grid, (i, j)


def get_steps_from_start(grid, start) -> Counter[tuple[int, int], int]:
    def get_direction(prev_pos, curr_pos):
        i_diff = curr_pos[0] - prev_pos[0]
        j_diff = curr_pos[1] - prev_pos[1]
        step = (i_diff, j_diff)
        if step == (-1, 0):
            return "north"
        if step == (1, 0):
            return "south"
        if step == (0, -1):
            return "west"
        if step == (0, 1):
            return "east"

    def get_next_pos(curr_pos, last_direction):
        i, j = curr_pos
        tile = grid[i, j]
        if tile.north and last_direction != "south":
            return (i - 1, j), "north"
        if tile.south and last_direction != "north":
            return (i + 1, j), "south"
        if tile.east and last_direction != "west":
            return (i, j + 1), "east"
        if tile.west and last_direction != "east":
            return (i, j - 1), "west"
        else:
            raise RuntimeError()

    def get_circuit(direction):
        distance = Counter()
        i, j = start
        pos = deque(maxlen=2)
        for step in count():
            if grid[i, j].is_start and len(pos) > 0:
                break
            assert (i, j) not in distance or len(pos) == 0
            distance[(i, j)] = step
            pos.append((i, j))
            (i, j), direction = get_next_pos((i, j), direction)
        
    steps_from_start = Counter()
    if grid[*start].north:
        steps_from_start = steps_from_start | get_circuit("north")
    if grid[*start].south:
        steps_from_start = steps_from_start | get_circuit("south")
    if grid[*start].west:
        steps_from_start = steps_from_start | get_circuit("west")
    if grid[*start].east:
        steps_from_start = steps_from_start | get_circuit("east")

    return steps_from_start


def main():
    with open("10-example.in") as f:
        grid, start = parse(f)

    step: Counter[tuple[int, int], int] = get_steps_from_start(grid, start)
    print(step.most_common(1))


if __name__ == "__main__":
    main()
