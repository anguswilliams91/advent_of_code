"""Solution to day one."""
from typing import Sequence

from pathlib import Path


def load_input(path: Path) -> Sequence[int]:
    """Loads the input data for the puzzle."""
    with open(path, "r") as f:
        depths = tuple(int(d) for d in f.readlines())
    return depths


def count_number_of_depth_increases(depths: Sequence[int]) -> int:
    """Counts the number of times depth increases in a sequence of sonar measurements."""
    depth_changes = [x - y for x, y in zip(depths[1:], depths[:-1])]
    return sum(d > 0 for d in depth_changes)


if __name__ == "__main__":
    depths = load_input(Path("input.txt"))
    print(count_number_of_depth_increases(depths))