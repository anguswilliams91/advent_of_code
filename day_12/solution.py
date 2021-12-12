"""12. Passage pathing."""

from collections import defaultdict
import copy
from typing import Collection, Mapping

Cave = str
CaveMap = str
CaveSystem = Mapping[str, Collection[str]]


def parse_cave_map(cave_map: CaveMap) -> CaveSystem:
    """Parses a cave map into a graph representing the cave system."""
    cave_system = defaultdict(set)
    for connection in cave_map.splitlines():
        first_cave, second_cave = connection.split("-")
        cave_system[first_cave].add(second_cave)
        cave_system[second_cave].add(first_cave)
    return cave_system


def find_num_routes_from_cave_to_end(
    cave: Cave,
    cave_system: CaveSystem,
    visited_caves: Collection[Cave],
    small_cave_has_been_revisited: bool,
):
    """Finds the number of routes from the given cave in the system to the end."""
    if cave == "end":
        return 1
    else:

        def cave_is_eligible(c):
            is_eligible = c.isupper()
            if small_cave_has_been_revisited:
                return is_eligible or c not in visited_caves
            else:
                return is_eligible or (c.islower() and c != "start")

        eligible_caves = [c for c in cave_system[cave] if cave_is_eligible(c)]
        if not eligible_caves:
            return 0
        else:
            return sum(
                find_num_routes_from_cave_to_end(
                    c,
                    cave_system,
                    visited_caves | {cave},
                    small_cave_has_been_revisited
                    or (c.islower() and c in visited_caves),
                )
                for c in eligible_caves
            )


def find_number_of_paths_from_start_to_end(
    cave_map: CaveMap, no_returns_allowed: bool = True
) -> int:
    """Finds the number of paths from the start to the end given a map.
    
    If a single small cave is allowed to be visited twice, no_returns_allowed is False.
    """
    cave_system = parse_cave_map(cave_map)
    return find_num_routes_from_cave_to_end(
        "start", cave_system, set(), no_returns_allowed
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        cave_map = f.read()

    part_one = find_number_of_paths_from_start_to_end(cave_map)
    part_two = find_number_of_paths_from_start_to_end(
        cave_map, no_returns_allowed=False
    )
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
