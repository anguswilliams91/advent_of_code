"""4. Giant squid."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, NamedTuple, Sequence

import numpy as np


@dataclass
class BingoBoard:
    """Represents a bingo board as a grid of numbers."""

    numbers: np.ndarray
    marked: np.ndarray = field(init=False)

    def __post_init__(self):
        self.marked = np.zeros_like(self.numbers, dtype=bool)

    @classmethod
    def from_string(cls, number_grid: str) -> BingoBoard:
        rows = number_grid.splitlines()
        board_size = len(rows)
        numbers = np.zeros((board_size, board_size), dtype=int)
        for row_number, row in enumerate(rows):
            for column_number, n in enumerate(row.split()):
                numbers[row_number, column_number] = int(n)

        return cls(numbers=numbers)


class BingoGame(NamedTuple):
    boards: Sequence[BingoBoard]
    numbers_to_draw: Iterable[int]

    @classmethod
    def from_string(cls, sheet: str) -> BingoGame:
        """Converts a string representing a bingo game into a BingoGame."""
        game = sheet.split("\n\n")
        numbers_to_draw = (int(n) for n in game.pop(0).split(","))
        boards = tuple(BingoBoard.from_string(b) for b in game)
        return cls(boards=boards, numbers_to_draw=numbers_to_draw)


def play_bingo(sheet: str, let_octopus_win: bool) -> int:
    """Plays bingo using a set of boards and numbers to draw."""
    game = BingoGame.from_string(sheet)
    boards_that_have_won = set()
    for n in game.numbers_to_draw:
        for i, board in enumerate(game.boards):
            board.marked[board.numbers == n] = True
            is_winner = any(np.all(board.marked, axis=0)) or any(
                np.all(board.marked, axis=1)
            )
            winning_total = board.numbers[~board.marked].sum() * n

            if is_winner:
                if not let_octopus_win:
                    return winning_total
                else:
                    if (
                        i not in boards_that_have_won
                        and len(boards_that_have_won) == len(game.boards) - 1
                    ):
                        return winning_total
                    else:
                        boards_that_have_won.add(i)

    raise ValueError("Nobody wins!")


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        sheet = f.read()

    print(f"Part one: {play_bingo(sheet, let_octopus_win=False)}")
    print(f"Part two: {play_bingo(sheet, let_octopus_win=True)}")
