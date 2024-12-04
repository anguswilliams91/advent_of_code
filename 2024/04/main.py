"""Day 4: Ceres Search"""

from collections import defaultdict
from dataclasses import dataclass

_R = range(1, 4)

Point = tuple[int, int]


@dataclass
class WordSearch:
    grid: defaultdict[Point, str]
    width: int
    height: int

    def search_xmas(self, p: Point) -> int:
        n = 8
        for locs in (
            [(p[0] - i, p[1]) for i in _R],
            [(p[0] + i, p[1]) for i in _R],
            [(p[0], p[1] - i) for i in _R],
            [(p[0], p[1] + i) for i in _R],
            [(p[0] + i, p[1] + i) for i in _R],
            [(p[0] - i, p[1] - i) for i in _R],
            [(p[0] + i, p[1] - i) for i in _R],
            [(p[0] - i, p[1] + i) for i in _R],
        ):
            for l, c in zip(locs, "MAS"):
                if self.grid[l] != c:
                    n -= 1
                    break
        return n

    def search_x_mas(self, p: Point) -> bool:
        return (
            (
                self.grid[(p[0] - 1, p[1] + 1)] == "M"
                and self.grid[(p[0] + 1, p[1] - 1)] == "S"
            )
            or (
                self.grid[(p[0] - 1, p[1] + 1)] == "S"
                and self.grid[(p[0] + 1, p[1] - 1)] == "M"
            )
        ) and (
            (
                self.grid[(p[0] - 1, p[1] - 1)] == "M"
                and self.grid[(p[0] + 1, p[1] + 1)] == "S"
            )
            or (
                self.grid[(p[0] - 1, p[1] - 1)] == "S"
                and self.grid[(p[0] + 1, p[1] + 1)] == "M"
            )
        )


def load_input(path: str) -> WordSearch:
    ws = defaultdict(lambda: "")
    width = 0
    height = 0
    with open(path, "r") as f:
        for j, l in enumerate(f.readlines()):
            height += 1
            width = len(l)
            for i, c in enumerate(l):
                ws[(i, j)] = c
    return WordSearch(grid=ws, width=width, height=height)


def solve(ws: WordSearch) -> tuple[int, int]:
    n_xmas = 0
    n_x_mas = 0
    for i in range(ws.width):
        for j in range(ws.height):
            if ws.grid[(i, j)] == "X":
                n_xmas += ws.search_xmas((i, j))
            if ws.grid[(i, j)] == "A":
                n_x_mas += ws.search_x_mas((i, j))
    return n_xmas, n_x_mas


def main():
    ws = load_input("input.txt")
    part_one, part_two = solve(ws)
    print(f"Part 1: {part_one}")
    print(f"Part 2: {part_two}")


if __name__ == "__main__":
    main()
