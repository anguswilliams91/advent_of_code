"""11. Dumbo Octopus."""

from collections import deque
from typing import Sequence, Tuple

import numpy as np


OctopusGrid = np.ndarray


def get_neighbours(point: Tuple[int, int]) -> Sequence[Tuple[int, int]]:
    """Finds the neighbours of a point in 10x10 grid (including diagonals)."""
    r, c = point
    neighbours = []
    if r > 0:
        neighbours.append((r - 1, c))
        if c > 0:
            neighbours.append((r - 1, c - 1))
        if c < 9:
            neighbours.append((r - 1, c + 1))
    if r < 9:
        neighbours.append((r + 1, c))
        if c > 0:
            neighbours.append((r + 1, c - 1))
        if c < 9:
            neighbours.append((r + 1, c + 1))
    if c > 0:
        neighbours.append((r, c - 1))
    if c < 9:
        neighbours.append((r, c + 1))
    return tuple(neighbours)


def simulate_time_step(octopus_grid: OctopusGrid) -> Tuple[OctopusGrid, int]:
    """Evolves the octopus grid forward by a single time step and counts the flashes."""
    num_flashes = 0
    octopus_grid += 1
    flash_queue = deque(zip(*np.where(octopus_grid > 9)))
    has_flashed = set()
    while flash_queue:
        flashing_octopus = flash_queue.pop()
        if flashing_octopus not in has_flashed:
            has_flashed.add(flashing_octopus)
            neighbours = get_neighbours(flashing_octopus)
            for octopus in neighbours:
                octopus_grid[octopus] += 1
                if octopus_grid[octopus] > 9:
                    flash_queue.appendleft(octopus)
            num_flashes += 1
    for octopus in has_flashed:
        octopus_grid[octopus] = 0
    return octopus_grid, num_flashes


def parse_octopus_grid_description(octopus_grid_description: str) -> OctopusGrid:
    """Parses a string representing an octopus grid into an OctopusGrid."""
    return np.array(
        [[i for i in row] for row in octopus_grid_description.splitlines()], dtype=int
    )


def calculate_number_of_flashes_after_time_steps(
    octopus_grid_description: str, num_steps: int
) -> int:
    """Calculates the total number of flashes from octopuses in the given time."""
    octopus_grid = parse_octopus_grid_description(octopus_grid_description)
    num_flashes = 0
    for _ in range(num_steps):
        octopus_grid, num_flashes_this_step = simulate_time_step(octopus_grid)
        num_flashes += num_flashes_this_step
    return num_flashes


def find_first_time_step_of_synchronised_flash(octopus_grid_description: str) -> int:
    """Finds the first time when all the octopuses flash at once."""
    octopus_grid = parse_octopus_grid_description(octopus_grid_description)
    simultaneous_flash_has_occurred = False
    num_timesteps = 0
    while not simultaneous_flash_has_occurred:
        num_timesteps += 1
        octopus_grid, num_flashes_this_step = simulate_time_step(octopus_grid)
        simultaneous_flash_has_occurred = num_flashes_this_step == 100

    return num_timesteps


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        octopus_grid_description = f.read()

    part_one = calculate_number_of_flashes_after_time_steps(
        octopus_grid_description, 100
    )
    part_two = find_first_time_step_of_synchronised_flash(octopus_grid_description)
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")

