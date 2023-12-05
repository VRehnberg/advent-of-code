from __future__ import annotations

import re
from typing import IO, Iterable, TypeVar

from tqdm import tqdm


T = TypeVar("T")

re_map_header = re.compile(r"^([a-z]+)-to-([a-z]+) map:")


def grouper(iterable: Iterable[T], n: int) -> Iterable[tuple[T, T]]:
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3) --> ABC DEF ValueError
    # grouper('ABCDEF', 3) --> ABC DEF
    # Adapted from itertools recipy
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


class Map():
    def __init__(
            self,
            map_from: str,
            map_to: str,
            from_range: Iterable[range],
            shift: Iterable[int]
        ):
            self.map_from = map_from
            self.map_to = map_to
            self.from_range = from_range
            self.shift = shift

    @classmethod
    def from_file(cls, file: IO) -> Map:
        # Parse header for map group
        line = next(file).strip()
        map_header = re_map_header.match(line)
        if map_header is None:
            raise RuntimeError("File location does not start with header.")

        map_from = map_header.group(1)
        map_to = map_header.group(2)

        # Parse ranges
        mapping = []
        for line in file:
            line = line.strip()
            if not line:
                break

            mapping.append(tuple(map(int, line.split())))

        from_range: list[range] = []
        shift: list[int] = []
        for to_start, from_start, span in sorted(mapping, key=lambda tfs: tfs[1]):
            from_range.append(range(from_start, from_start + span))
            shift.append(to_start - from_start)

        return cls(
            map_from=map_from,
            map_to=map_to,
            from_range=from_range,
            shift=shift,
        )

    def __call__(self, from_value: Iterable[range]) -> Iterable[range]:
        for value_range in from_value:
            for from_range, shift in zip(self.from_range, self.shift):
                if value_range.stop <= from_range.start:
                    # Not affected, yield as is
                    yield value_range
                    value_range = None
                    break
                elif value_range.start <= from_range.start:
                    yield range(value_range.start, from_range.start)
                    value_range = range(from_range.start, value_range.stop)

                if value_range.start in from_range:
                    # Some shift will be needed
                    if value_range.stop in from_range:
                        # Shift full range
                        yield range(value_range.start + shift, value_range.stop + shift)
                        value_range = None
                        break
                    else:
                        # Shift part until stop
                        yield range(value_range.start + shift, from_range.stop + shift)
                        value_range = range(from_range.stop, value_range.stop)
                
            if value_range is not None:
                yield value_range


def parse_input(file: IO, seed_range: bool) -> tuple[Iterable[int] | list[range], dict[str, Map]]:
    # Parse seeds
    seed_line = next(file).strip()
    name, seed_str = seed_line.split(":")
    assert name == "seeds"
    if not seed_range:
        seeds = [int(s) for s in seed_str.strip().split()]
    else:
        seeds = [
            range(int(seed_start), int(seed_start) + int(seed_length))
            for seed_start, seed_length in grouper(seed_str.strip().split(), 2)
        ]

    # Skip blank line
    blank_line = next(file).strip()
    if blank_line:
        raise RuntimeError(f'Expected line to be blank, is "{blank_line}"')

    # Parse maps
    maps: dict[str, Map] = {}
    while True:
        try:
            m = Map.from_file(file)
            maps[m.map_from] = m
        except StopIteration:
            break

    return seeds, maps


def main():
    with open("5.in") as f:
        seeds, maps = parse_input(f, seed_range=True)

    # Keep smallest seen location
    values = seeds
    unit = "seed"
    while unit != "location":
        mapping = maps[unit]
        #print(unit, values, mapping.from_range, mapping.shift)
        values = list(mapping(values))
        #assert sum(map(len, values)) == 27
        unit = mapping.map_to
    #print(unit, values, mapping.from_range, mapping.shift)
        
    print("Minimum location:", min(range.start for range in values if len(range) >= 1))


if __name__ == "__main__":
    main()
