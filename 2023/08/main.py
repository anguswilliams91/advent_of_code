"""Day 8: Haunted Wasteland"""
from __future__ import annotations

import math


def parse_map(map: str) -> tuple(list[str], dict[str, dict[str, str]]):
    """Parses a map into instructions and nodes."""
    lines = map.splitlines()
    instructions = list(lines[0])
    node_to_instruction = {}
    for line in lines[2:]:
        origin, lr_nodes = line.split(" = ")
        left, right = lr_nodes.strip("()").split(", ")
        node_to_instruction[origin] = {"L": left, "R": right}
    return instructions, node_to_instruction


def count_steps_for_humans(
    instructions: list[str], node_to_instruction: dict[str, dict[str, str]]
) -> int:
    """Finds how many steps are needed to reach ZZZ from AAA."""
    num_steps = 0
    num_instructions = len(instructions)
    node = "AAA"
    while node != "ZZZ":
        instruction = instructions[num_steps % num_instructions]
        node = node_to_instruction[node][instruction]
        num_steps += 1
    return num_steps


def single_ghost_trajectory(
    node: str, instructions: list[str], node_to_instruction: dict[str, dict[str, str]]
) -> list[int]:
    """Finds the number of steps it takes for a single ghost to reach Z nodes."""
    z_visited = set()
    reaches_z_after = []
    num_steps = 0
    num_instructions = len(instructions)
    while True:
        instruction = instructions[num_steps % num_instructions]
        node = node_to_instruction[node][instruction]
        num_steps += 1
        if node.endswith("Z"):
            if (instruction, node) in z_visited:
                # We've been here before, so this is a cycle.
                break
            reaches_z_after.append(num_steps)
            z_visited.add((instruction, node))
    return reaches_z_after


def count_steps_for_ghosts(
    instructions: list[str], node_to_instruction: dict[str, dict[str, str]]
) -> dict[str, list[int]]:
    """Gets the ghost trajectories from all A nodes."""
    ghost_steps = {
        node: single_ghost_trajectory(node, instructions, node_to_instruction)
        for node in node_to_instruction
        if node.endswith("A")
    }
    # There's only one route per starting node.
    steps = [s[0] for s in ghost_steps.values()]
    return math.lcm(*steps)


def solve(map: str) -> tuple[int, int]:
    """Solves both parts of the puzzle."""
    instructions, node_to_instruction = parse_map(map)
    human_steps = count_steps_for_humans(instructions, node_to_instruction)
    ghost_steps = count_steps_for_ghosts(instructions, node_to_instruction)
    return human_steps, ghost_steps


def main():
    with open("input.txt", "r") as f:
        map = f.read()

    human_steps, ghost_steps = solve(map)
    print("Part 1: ", human_steps)
    print("Part 2: ", ghost_steps)


if __name__ == "__main__":
    main()
