"""13. Transparent Origami."""

from __future__ import annotations

from dataclasses import dataclass
import re

import numpy as np
from numpy.lib.function_base import flip

_FOLD_INSTRUCTION = re.compile(r"fold along ([xy])=(\d+)")


@dataclass
class TransparentPaper:
    """Transparent paper with some dots on it."""
    dots: np.ndarray

    def __str__(self):
        return "\n".join(
            "".join("#" if i == 1 else "." for i in row) for row in self.dots
        )
    
    def __repr__(self):
        return str(self)

    @classmethod
    def from_string(cls, description: str) -> TransparentPaper:
        coords_with_dots = []
        for row in description.splitlines():
            y, x = row.split(",")
            coords_with_dots.append((int(x), int(y)))
        (x_max, y_max) = (
            max(coord[i] for coord in coords_with_dots) for i in (0, 1)
        )
        dots = np.zeros((x_max + 1, y_max + 1), dtype=int)
        for coord in coords_with_dots:
            dots[coord] = 1
        return cls(dots=dots)


def fold_paper(instruction: str, paper: TransparentPaper) -> TransparentPaper:
    """Folds the paper according to the instruction."""
    dimension, row_or_column = _FOLD_INSTRUCTION.match(instruction).groups()
    match dimension:
        case "x":
            column = int(row_or_column)
            flipped = np.flip(paper.dots[:, column:], 1)
            unflipped = paper.dots[:, :column + 1]
            if (d := flipped.shape[1] - unflipped.shape[1]) > 0:
                new_dots = np.pad(unflipped, ((0, 0), (d, 0))) | flipped
            elif d < 0:
                new_dots = unflipped | np.pad(flipped, ((0, 0), (-d, 0)))
            else:
                new_dots = unflipped | flipped
            new_dots = new_dots[:, :-1]
        case "y":
            row = int(row_or_column)
            flipped = np.flip(paper.dots[row:, :], 0)
            unflipped = paper.dots[:row + 1, :]
            if (d := flipped.shape[0] - unflipped.shape[0]) > 0:
                new_dots = np.pad(unflipped, ((d, 0), (0, 0))) | flipped
            elif d < 0:
                new_dots = unflipped | np.pad(flipped, ((-d, 0), (0, 0)))
            else:
                new_dots = unflipped | flipped
            new_dots = new_dots[:-1, :]
        case _:
            raise ValueError(f"Unexpected dimension {dimension}.")
    return TransparentPaper(dots=new_dots)



def count_number_of_visible_dots_after_first_fold(manual: str) -> int:
    """Counts the number of dots visible after the first fold in the manual."""
    dots_description, instructions = manual.split("\n\n")
    paper = TransparentPaper.from_string(dots_description)
    paper = fold_paper(instructions.splitlines()[0], paper)
    return paper.dots.sum()


def follow_all_instructions(manual: str) -> TransparentPaper:
    """Folds the paper according to all of the instructions in the manual."""
    dots_description, instructions = manual.split("\n\n")
    paper = TransparentPaper.from_string(dots_description)
    for fold in instructions.splitlines():
        paper = fold_paper(fold, paper)
    return paper
          


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        manual = f.read()
    
    part_one = count_number_of_visible_dots_after_first_fold(manual)
    print(f"Part one: {part_one}")
    part_two = follow_all_instructions(manual)
    print(f"Part two: \n{part_two}")