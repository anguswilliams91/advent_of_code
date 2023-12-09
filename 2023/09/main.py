"""Day 9: Mirage Maintenance"""


def calculate_diff(history: list[int]) -> list[int]:
    """Gets the diff of a sequence with itself."""
    return [next - curr for curr, next in zip(history[:-1], history[1:])]


def extrapolate(history: list[int], backwards: bool) -> int:
    """Extrapolates a sequence forwards or backwards."""
    diffs = []
    curr = history
    while not all([c == 0 for c in curr]):
        diff = calculate_diff(curr)
        diffs.append(diff)
        curr = diff
    diffs.reverse()
    seqs = diffs[1:]
    seqs.append(history)
    extrapolation = 0
    for seq in seqs:
        if backwards:
            extrapolation = seq[0] - extrapolation
        else:
            extrapolation = seq[-1] + extrapolation
    return extrapolation


def parse_input(report: str) -> list[list[int]]:
    """Parses a report into a list of histories."""
    histories = []
    for line in report.splitlines():
        histories.append([int(n) for n in line.split()])
    return histories


def solve(report: str) -> tuple[int, int]:
    """Finds the sum of the extrapolations forwards and backwards."""
    histories = parse_input(report)
    part_one = sum(extrapolate(h, False) for h in histories)
    part_two = sum(extrapolate(h, True) for h in histories)
    return part_one, part_two


def main():
    with open("input.txt", "r") as f:
        report = f.read()

    part_one, part_two = solve(report)

    print("Part 1: ", part_one)
    print("Part 1: ", part_two)


if __name__ == "__main__":
    main()
