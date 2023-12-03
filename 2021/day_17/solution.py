"""17. Trick shot."""

from dataclasses import dataclass
import math
from typing import Sequence


@dataclass
class Solution:
    u_0: int
    v_0: int
    highest_point: int


def calculate_solutions(
    y_min: int, y_max: int, x_min: int, x_max: int
) -> Sequence[Solution]:
    solutions = []
    for u_0 in range(1, x_max + 1):
        for v_0 in range(y_min, -y_min + 1):
            x, y = 0, 0
            u, v = u_0, v_0
            highest_point = y
            while x <= x_max and y >= y_min:
                x, y = x + u, y + v
                u, v = max(0, u - 1), v - 1
                if y > highest_point:
                    highest_point = y
                if (x_min <= x <= x_max) and (y_min <= y <= y_max):
                    solutions.append(
                        Solution(u_0=u_0, v_0=v_0, highest_point=highest_point)
                    )
                    break
    return solutions


def calculate_highest_possible_y_coordinate(
    y_min: int, y_max: int, x_min: int, x_max: int
) -> int:
    return max(s.highest_point for s in calculate_solutions(y_min, y_max, x_min, x_max))


def calculate_number_of_solutions(
    y_min: int, y_max: int, x_min: int, x_max: int
) -> int:
    return len(calculate_solutions(y_min, y_max, x_min, x_max))


if __name__ == "__main__":
    print(f"Part one: {calculate_highest_possible_y_coordinate(-171, -136, 60, 94)}")
    print(f"Part two: {calculate_number_of_solutions(-171, -136, 60, 94)}")
