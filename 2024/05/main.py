"""Day 5: Print Queue"""

from collections import defaultdict
from functools import cmp_to_key


def load_input(path):
    with open(path, "r") as f:
        text = f.read()
        rules_text, sequences_text = text.split("\n\n")
    rules = defaultdict(lambda: set())
    for rule in rules_text.splitlines():
        l, r = rule.split("|")
        rules[int(l)].add(int(r))
    sequences = []
    for sequence in sequences_text.splitlines():
        sequences.append([int(i) for i in sequence.split(",")])
    return sequences, rules


def is_in_order(sequence, rules):
    seen = set()
    for i in sequence:
        if seen & rules[i]:
            return False
        seen.add(i)
    return True


def sorted_by_rules(sequence, rules):
    def cmp(i, j):
        if i in rules[j]:
            return 1
        if j in rules[i]:
            return -1
        return 0

    return sorted(sequence, key=cmp_to_key(cmp))


def solve(sequences, rules):
    part_one = 0
    part_two = 0
    for s in sequences:
        if is_in_order(s, rules):
            part_one += s[len(s) // 2]
            continue
        part_two += sorted_by_rules(s, rules)[len(s) // 2]
    return part_one, part_two


def main():
    sequences, rules = load_input("input.txt")
    part_one, part_two = solve(sequences, rules)
    print(f"Part 1: {part_one}")
    print(f"Part 1: {part_two}")


if __name__ == "__main__":
    main()
