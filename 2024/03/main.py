"""Day 3: Mull It Over"""

import re


def load_input(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def part_one(memory: str) -> int:
    sum = 0
    for m in re.finditer(r"mul\((\d+),(\d+)\)", memory):
        sum += int(m.group(1)) * int(m.group(2))
    return sum


def part_two(memory: str) -> int:
    sum = 0
    enabled = True
    for m in re.finditer(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)", memory):
        match m.group(0):
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                sum += enabled * int(m.group(1)) * int(m.group(2))
    return sum


def main():
    memory = load_input("input.txt")
    print(f"Part 1: {part_one(memory)}")
    print(f"Part 2  : {part_two(memory)}")


if __name__ == "__main__":
    main()
