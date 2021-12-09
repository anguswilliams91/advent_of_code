"""9. Smoke basin."""

from functools import reduce
from typing import List, Sequence, Tuple

import numpy as np

HeightMap = np.ndarray


def get_neighbours(r: int, c: map, height_map: HeightMap) -> Sequence[Tuple[int, int]]:
    length, breadth = height_map.shape
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


def is_a_low_point(r: int, c: int, height_map: HeightMap) -> bool:
    """Determines if a point is a low point."""
    point = height_map[r, c]
    neighbours = get_neighbours(r, c, height_map)
    return reduce(
        lambda x, y: x and y,
        (point < height_map[neighbour] for neighbour in neighbours),
    )


def parse_map_desription(height_map_description: str) -> HeightMap:
    """Parses the height map into an array."""
    height_map = []
    for description_row in height_map_description.splitlines():
        row = []
        for n in description_row:
            row.append(int(n))
        height_map.append(row)
    return np.array(height_map)


def find_low_points(height_map: HeightMap) -> List[int]:
    """Finds the low points and sums them."""
    low_points = []
    length, breadth = height_map.shape
    for r in range(length):
        for c in range(breadth):
            if is_a_low_point(r, c, height_map):
                low_points.append((r, c))

    return low_points


def sum_of_low_points(height_map_description: str) -> int:
    height_map = parse_map_desription(height_map_description)
    return sum(height_map[p] + 1 for p in find_low_points(height_map))


def find_basin_sizes(height_map_description: str) -> Sequence[int]:
    height_map = parse_map_desription(height_map_description)
    low_points = find_low_points(height_map)
    basin_sizes = []

    def find_points_in_basin(point, height_map):
        r, c = point
        neighbours = get_neighbours(r, c, height_map)
        points_in_basin = {point}
        for neighbour in neighbours:
            if height_map[neighbour] > height_map[point] and height_map[neighbour] != 9:
                points_in_basin = points_in_basin | find_points_in_basin(
                    neighbour, height_map
                )
        return points_in_basin

    for low_point in low_points:
        basin_sizes.append(len(find_points_in_basin(low_point, height_map)))

    return basin_sizes


def product_of_biggest_basins(height_map_description: str) -> int:
    basin_sizes = find_basin_sizes(height_map_description)
    return reduce(lambda x, y: x * y, list(reversed(sorted(basin_sizes)))[:3])


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        height_map_description = f.read()

    print(f"Part one: {sum_of_low_points(height_map_description)}")
    print(f"Part two: {product_of_biggest_basins(height_map_description)}")
