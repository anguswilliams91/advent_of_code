"""Solution to day one."""
from typing import Sequence

from pathlib import Path


def load_input(path: Path) -> Sequence[int]:
    """Loads the input data for the puzzle."""
    with open(path, "r") as f:
        depths = tuple(int(d) for d in f.readlines())
    return depths


def count_number_of_depth_increases(depths: Sequence[int], window_size: int = 1) -> int:
    """Counts the number of times depth increases in a sequence of sonar measurements."""
    depth_changes = (
        sum(depths[i : i + window_size]) - sum(depths[i - 1 : i - 1 + window_size])
        for i in range(1, len(depths) - window_size + 1)
    )
    return sum(d > 0 for d in depth_changes)


if __name__ == "__main__":
    depths = load_input(Path("input.txt"))
    print(f"Part one: {count_number_of_depth_increases(depths, window_size=1)}")
    print(f"Part two: {count_number_of_depth_increases(depths, window_size=3)}")
