from collections import Counter
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
                west=False,
                east=True,
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

    def get_start_directions(self):
        directions = []
        if not self.north:
            directions.append("north")
        if not self.south:
            directions.append("south")
        if not self.west:
            directions.append("west")
        if not self.east:
            directions.append("east")
        return directions


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


class MyDict(Counter):
    def __missing__(self, key):
        # Only want some aspects of counter
        raise KeyError

    def __or__(self, other):
        '''Union is the minimum of value in either of the input counters.
        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 1, 'c': 2, 'a': 1})
        '''
        if not isinstance(other, Counter):
            return NotImplemented

        result = MyDict()
        for elem, count in self.items():
            other_count = other[elem]
            result[elem] = count if count < other_count else other_count
        for elem, count in other.items():
            if elem not in self:
                result[elem] = count
        return result


def get_steps_from_start(grid, start) -> MyDict[tuple[int, int], int]:
    def get_next_pos(pos, last_direction):
        i, j = pos
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
        #print("---------------", start)
        distance = MyDict()
        pos = None
        for step in count():
            if pos is None:
                pos = start
            elif grid[*pos].is_start:
                break
            else:
                assert pos not in distance
            distance[pos] = step
            prev_dir = direction
            pos, direction = get_next_pos(pos, direction)
            #print(step, pos, prev_dir, direction)
        return distance

    def get_loop(direction):
        loop = [start]
        for step in count():
            if pos is None:
                pos = start
            elif grid[*pos].is_start:
                break
            else:
                assert pos not in distance
            pos, direction = get_next_pos(pos, direction)
            loop.append(pos)
        return loop
        
    steps_from_start = MyDict()
    for direction in grid[*start].get_start_directions():
        print(direction)
        steps_from_start = steps_from_start | get_circuit(direction)
    loop = get_loop(direction)

    return steps_from_start


def main():
    with open("10.in") as f:
        grid, start = parse(f)
    print(grid)

    steps: MyDict[tuple[int, int], int], loop = get_steps_from_start(grid, start)
    print(steps.most_common(1))
    str_grid = np.full_like(grid, fill_value=".", dtype=str)
    for (i, j), n in steps.items():
        str_grid[i, j] = f"{n}"
    print(str_grid)



if __name__ == "__main__":
    main()
