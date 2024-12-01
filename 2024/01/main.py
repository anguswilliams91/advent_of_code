"""Day 1: Historian Hysteria"""
from collections.abc import Sequence

from collections import Counter

def load_input(path: str) -> tuple[Sequence[int], Sequence[int]]:
    ls, rs = [], []
    with open(path, "r") as f:
        for line in f.readlines():
            l, r = line.split()
            ls.append(int(l))
            rs.append(int(r))
    return (ls, rs)

def part_one(ls, rs) -> int:
    ls, rs = sorted(ls), sorted(rs)
    ds = [abs(l-r) for l,r in zip(ls, rs)]
    return sum(ds)

def part_two(ls, rs) -> int:
    rcounts = Counter(rs)
    similarity = 0
    for l in ls:
        similarity += l * rcounts[l]
    return similarity

def solve(ls, rs) -> tuple[int, int]:
    return part_one(ls, rs), part_two(ls, rs)

def main():
    ls, rs = load_input("input.txt")
    p1, p2 = solve(ls, rs)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    
if __name__ == "__main__":
    main()