"""Day 4: Scratchcards"""

type Scratchcard = tuple[set[int], set[int]]


def parse_input(scratchcards_text: str) -> list[Scratchcard]:
    """Converts a text representation of some scratchcards into a list of Scratchcards."""
    scratchcards = []
    for s in scratchcards_text.splitlines():
        numbers_text = s.split(":")[1].strip()
        winners_text, actual_text = numbers_text.split("|")
        winners = set(int(w) for w in winners_text.strip().split())
        actual = set(int(a) for a in actual_text.strip().split())
        scratchcards.append((winners, actual))
    return scratchcards


def solve(scratchcards_text: str) -> int:
    """Calculates the points total (part 1) and the total # of scratchcards (part 2)."""
    scratchcards = parse_input(scratchcards_text)
    points = 0
    copies = [1] * len(scratchcards)
    for i, scratchcard in enumerate(scratchcards):
        winners, actual = scratchcard
        if num_winners := len(set(winners) & set(actual)):
            points += 2 ** (num_winners - 1)
            for j in range(i + 1, i + 1 + num_winners):
                copies[j] += copies[i]
    return points, sum(copies)


def main():
    with open("input.txt", "r") as f:
        scratchcards_text = f.read()

    points, total_scratchcards = solve(scratchcards_text)

    print("Part 1: ", points)
    print("Part 2: ", total_scratchcards)


if __name__ == "__main__":
    main()