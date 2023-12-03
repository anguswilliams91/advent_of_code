"""15. Chiton."""

from heapq import heappop, heappush
from typing import Sequence, Tuple

import numpy as np

RiskMap = np.ndarray


def parse_risk_map(risk_map_description: str) -> RiskMap:
    """Parses a risk map string into an array."""
    return np.array(
        [[i for i in row] for row in risk_map_description.splitlines()], dtype=int
    )


def get_neighbours(
    point: Tuple[int, int], risk_map: RiskMap
) -> Sequence[Tuple[int, int]]:
    """Finds the neighbours of a point in a 2D rectangular grid."""
    length, breadth = risk_map.shape
    r, c = point
    neighbours = []
    if r > 0:
        neighbours.append((r - 1, c))
    if r < length - 1:
        neighbours.append((r + 1, c))
    if c < breadth - 1:
        neighbours.append((r, c + 1))
    if c > 0:
        neighbours.append((r, c - 1))
    return neighbours


def find_risk_of_path_with_lowest_total_risk(
    risk_map_description: str, use_full_map: bool
) -> int:
    """Uses Djikstra to find the risk of the points in the path with lowest total risk."""
    risk_map = (
        make_full_map(risk_map_description)
        if use_full_map
        else parse_risk_map(risk_map_description)
    )
    length, breadth = risk_map.shape
    tentative_risk = np.ones_like(risk_map) * np.inf
    tentative_risk[0, 0] = 0
    priority_queue = [(0, (0, 0))]
    while priority_queue:
        _, current_point = heappop(priority_queue)
        for neighbour in get_neighbours(current_point, risk_map):
            candidate_risk = tentative_risk[current_point] + risk_map[neighbour]
            if candidate_risk < tentative_risk[neighbour]:
                tentative_risk[neighbour] = candidate_risk
                heappush(priority_queue, (candidate_risk, neighbour))

    return tentative_risk[(length - 1, breadth - 1)]


def make_full_map(risk_map_description: str) -> RiskMap:
    """Makes the full map from the input by tiling it and adding risk."""
    base_map = parse_risk_map(risk_map_description)
    height, width = base_map.shape
    full_map = np.zeros((5 * height, 5 * width))
    for i in range(5):
        for j in range(5):
            full_map[
                height * i : height * (i + 1), width * j : width * (j + 1)
            ] = base_map + (i + j)
    full_map = full_map % 9
    full_map[full_map == 0] = 9
    return full_map


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        risk_map_description = f.read()

    part_one = find_risk_of_path_with_lowest_total_risk(
        risk_map_description, use_full_map=False
    )
    part_two = find_risk_of_path_with_lowest_total_risk(
        risk_map_description, use_full_map=True
    )
    print(f"Part one: {part_one}")
    print(f"Part one: {part_two}")
