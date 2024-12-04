"""Day 2: Red-Nosed Reports"""

from collections.abc import Sequence


def sign(d: int) -> int:
    if d < 0:
        return -1
    if d > 0:
        return 1
    return 0


def is_safe(report: Sequence[int]) -> bool:
    d_prev = report[1] - report[0]
    if not (1 <= abs(d_prev) <= 3):
        return False
    for r1, r2 in zip(report[1:-1], report[2:]):
        d_curr = r2 - r1
        if sign(d_curr) != sign(d_prev) or not (1 <= abs(d_curr) <= 3):
            return False
        d_prev = d_curr
    return True


def is_safe_dampened(report: Sequence[int]) -> bool:
    d_prev = report[1] - report[0]
    if not (1 <= abs(d_prev) <= 3):
        # We can remove the first entry or second entry
        return is_safe(report[1:]) or is_safe(report[:1] + report[2:])
    for i, (r1, r2) in enumerate(zip(report[1:-1], report[2:]), start=1):
        d_curr = r2 - r1
        if sign(d_curr) != sign(d_prev) or not (1 <= abs(d_curr) <= 3):
            # We can remove the last entry, the current entry or the next entry
            return (
                is_safe(report[: i - 1] + report[i:])
                or is_safe(report[:i] + report[i + 1 :])
                or is_safe(report[: i + 1] + report[i + 2 :])
            )
        d_prev = d_curr
    return True


def load_input(path: str) -> list[list[int]]:
    reports = []
    with open(path, "r") as f:
        for l in f.readlines():
            reports.append([int(i) for i in l.split()])
    return reports


def main():
    reports = load_input("input.txt")
    print(f"Part 1: {sum(is_safe(r) for r in reports)}")
    print(f"Part 2: {sum(is_safe_dampened(r) for r in reports)}")


if __name__ == "__main__":
    main()
