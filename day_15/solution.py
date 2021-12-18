"""15. Chiton."""

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


def find_risk_of_path_with_lowest_total_risk(risk_map_description: str) -> int:
    """Finds the risk of the path with the lowest total risk."""
    risk_map = parse_risk_map(risk_map_description)
    length, breadth = risk_map.shape
    unvisited_points = {(i, j) for i in range(length) for j in range(breadth)}
    tentative_risk = np.ones_like(risk_map) * np.inf
    tentative_risk[0, 0] = 0
    current_point = (0, 0)
    while (length - 1, breadth - 1) in unvisited_points:
        for neighbour in get_neighbours(current_point, risk_map):
            if neighbour in unvisited_points:
                candidate_risk = tentative_risk[current_point] + risk_map[neighbour]
                if candidate_risk < tentative_risk[neighbour]:
                    tentative_risk[neighbour] = candidate_risk
        unvisited_points.remove(current_point)
        current_point = sorted(unvisited_points, key=tentative_risk.__getitem__)[0]
    return tentative_risk[(length - 1, breadth - 1)]


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        risk_map_description = f.read()

    part_one = find_risk_of_path_with_lowest_total_risk(risk_map_description)
    print(f"Part one: {part_one}")
