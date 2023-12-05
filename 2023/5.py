from __future__ import annotations

import re
from typing import IO


re_map_header = re.compile(r"^([a-z]+)-to-([a-z]+) map:")


class Map():
    def __init__(
            self,
            map_from: str,
            map_to: str,
            mapping: list[tuple[int, int, int]]
        ):
            self.map_from = map_from
            self.map_to = map_to
            self.mapping = mapping

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

        return cls(
            map_from=map_from,
            map_to=map_to,
            mapping=mapping,
        )

    def __call__(self, from_value: int) -> int:
        for to_start, from_start, span in self.mapping:
            if (
                from_value >= from_start
                and from_value < (from_start + span)
            ):
                return to_start + (from_value - from_start)
        return from_value


def parse_input(file: IO) -> tuple[list[int], dict[str, Map]]:
    # Parse seeds
    seed_line = next(file).strip()
    name, seed_str = seed_line.split(":")
    assert name == "seeds"
    seeds = [int(s) for s in seed_str.strip().split()]

    # Skip blank line
    blank_line = next(file).strip()
    if blank_line:
        raise RuntimeError(f'Expected line to be blank, is "{blank_line}"')

    # Parse maps
    maps: dict[str, Map] = {}
    while True:
        try:
            m = Map.from_file(file)
        except StopIteration:
            break
        finally:
            maps[m.map_from] = m

    return seeds, maps


def main():
    with open("5.in") as f:
        seeds, maps = parse_input(f)


    # Get locations
    locations: list[int] = []
    values = seeds
    unit = "seed"
    while unit != "location":
        mapping = maps[unit]
        values = [mapping(v) for v in values]
        unit = mapping.map_to

    print("Minimum location:", min(values))


if __name__ == "__main__":
    main()
