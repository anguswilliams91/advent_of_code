"""5. Hydrothermal venture."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from typing import NamedTuple, Tuple


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, point: str) -> Point:
        x, y = (int(c) for c in point.split(","))
        return cls(x=x, y=y)


class LineType(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3


@dataclass
class Vent:
    start_point: Point
    end_point: Point
    line: Tuple[Point] = field(init=False)
    line_type: LineType = field(init=False)

    def __post_init__(self):
        if self.start_point.x == self.end_point.x:
            self.line_type = LineType.VERTICAL
            y_min, y_max = sorted([self.start_point.y, self.end_point.y])
            self.line = tuple(
                Point(x=self.start_point.x, y=y) for y in range(y_min, y_max + 1)
            )

        elif self.start_point.y == self.end_point.y:
            self.line_type = LineType.HORIZONTAL
            x_min, x_max = sorted([self.start_point.x, self.end_point.x])
            self.line = tuple(
                Point(x=x, y=self.start_point.y) for x in range(x_min, x_max + 1)
            )
        else:
            self.line_type = LineType.DIAGONAL
            x_direction = 1 if self.start_point.x < self.end_point.x else -1
            y_direction = 1 if self.start_point.y < self.end_point.y else -1
            self.line = tuple(
                Point(
                    x=self.start_point.x + x_direction * i,
                    y=self.start_point.y + y_direction * i,
                )
                for i in range(abs(self.start_point.x - self.end_point.x) + 1)
            )

    @classmethod
    def from_string(cls, vent: str) -> Vent:
        start, end = vent.split(" -> ")
        start_point = Point.from_string(start)
        end_point = Point.from_string(end)
        return cls(start_point=start_point, end_point=end_point)


def count_number_of_points_with_overlapping_lines(
    vents_description: str, use_diagonal: bool
) -> int:
    """Counts the number of points where multiple lines overlap."""
    vents = tuple(Vent.from_string(v) for v in vents_description.splitlines())
    legal_line_types = (
        tuple(LineType) if use_diagonal else (LineType.HORIZONTAL, LineType.VERTICAL)
    )
    lines_per_point = Counter(
        reduce(
            lambda a, b: a + b,
            (v.line for v in vents if v.line_type in legal_line_types),
        )
    )
    return sum(v > 1 for v in lines_per_point.values())


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        vents_description = f.read()

    part_one = count_number_of_points_with_overlapping_lines(
        vents_description, use_diagonal=False
    )
    part_two = count_number_of_points_with_overlapping_lines(
        vents_description, use_diagonal=True
    )
    print(f"Part one: {part_one}")
    print(f"Part one: {part_two}")
