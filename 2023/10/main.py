"""Day 10: Pipe Maze"""

import collections
import math

Coordinate = tuple[int, int]


def parse_input(
    map_text: str,
) -> tuple[Coordinate, collections.defaultdict[Coordinate, str]]:
    coordinate_to_pipe = collections.defaultdict(lambda: ".")
    for i, line in enumerate(reversed(map_text.splitlines())):
        for j, pipe in enumerate(line):
            coordinate_to_pipe[(j, i)] = pipe
            if pipe == "S":
                start = (j, i)
    return start, coordinate_to_pipe


def get_neighbours(
    current: Coordinate, coordinate_to_pipe: dict[Coordinate, str]
) -> set[Coordinate]:
    connected = set()
    current_pipe = coordinate_to_pipe[current]
    x, y = current
    if current_pipe in ("|", "7", "F", "S") and coordinate_to_pipe[(x, y - 1)] in (
        "|",
        "L",
        "J",
    ):
        connected.add((x, y - 1))
    if current_pipe in ("|", "L", "J", "S") and coordinate_to_pipe[(x, y + 1)] in (
        "|",
        "7",
        "F",
    ):
        connected.add((x, y + 1))
    if current_pipe in ("-", "J", "7", "S") and coordinate_to_pipe[(x - 1, y)] in (
        "-",
        "L",
        "F",
    ):
        connected.add((x - 1, y))
    if current_pipe in ("-", "L", "F", "S") and coordinate_to_pipe[(x + 1, y)] in (
        "-",
        "J",
        "7",
    ):
        connected.add((x + 1, y))
    return connected


def breadth_first_search(
    start: Coordinate,
    coordinate_to_pipe: collections.defaultdict[Coordinate, str],
) -> set[Coordinate]:
    initial_neighbours = get_neighbours(start, coordinate_to_pipe)
    queue = [initial_neighbours.pop()]
    visited = set()
    while queue:
        current = queue.pop()
        visited.add(current)
        for neighbour in get_neighbours(current, coordinate_to_pipe):
            if neighbour not in visited:
                queue.append(neighbour)
            if neighbour == "S":
                break
    return visited


def solve(map_text: str) -> int:
    start, coordinate_to_pipe = parse_input(map_text)
    path = breadth_first_search(start, coordinate_to_pipe)
    furthest_away = math.ceil(len(path) / 2)
    return furthest_away


def main():
    with open("input.txt", "r") as f:
        map_text = f.read()

    max_steps = solve(map_text)
    print("Part 1: ", max_steps)


if __name__ == "__main__":
    main()
