"""Navigating a submarine."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Sequence, Union


class Direction(Enum):
    """Directions the submarine can be instructed to move."""

    FORWARD = 1
    DOWN = 2
    UP = 3


@dataclass
class Instruction:
    """Encodes an instruction to move the submarine."""

    direction: Direction
    distance: int


class SubmarinePositionWithoutAim:
    """Stores the location of a submarine and updates it according the part one rules."""

    def __init__(self, horizontal_position: int = 0, vertical_position: int = 0):
        self.horizontal_position = horizontal_position
        self.depth = vertical_position

    def follow_instruction(
        self, instruction: Instruction
    ) -> SubmarinePositionWithoutAim:
        """Moves the submarine according to an instruction."""
        if instruction.direction is Direction.FORWARD:
            self.horizontal_position += instruction.distance
        elif instruction.direction is Direction.DOWN:
            self.depth += instruction.distance
        elif instruction.direction is Direction.UP:
            self.depth -= instruction.distance
        else:
            raise ValueError("Unrecognised direction.")

        return self


class SubmarinePositionWithAim:
    """Stores the location of a submarine and updates it according the part two rules."""

    def __init__(
        self, horizontal_position: int = 0, vertical_position: int = 0, aim: int = 0
    ):
        self.horizontal_position = horizontal_position
        self.depth = vertical_position
        self.aim = aim

    def follow_instruction(
        self, instruction: Instruction
    ) -> SubmarinePositionWithoutAim:
        """Moves the submarine according to an instruction."""
        if instruction.direction is Direction.FORWARD:
            self.horizontal_position += instruction.distance
            self.depth += self.aim * instruction.distance
        elif instruction.direction is Direction.DOWN:
            self.aim += instruction.distance
        elif instruction.direction is Direction.UP:
            self.aim -= instruction.distance
        else:
            raise ValueError("Unrecognised direction.")

        return self


def parse_instructions(written_instructions: str) -> Sequence[Instruction]:
    """Parses a set of string instructions into Instructions."""
    instructions = []
    for written_instruction in written_instructions.splitlines():
        if written_instruction.startswith("forward"):
            direction = Direction.FORWARD
        elif written_instruction.startswith("down"):
            direction = Direction.DOWN
        elif written_instruction.startswith("up"):
            direction = Direction.UP
        else:
            raise ValueError("Unrecognised direction.")

        instructions.append(
            Instruction(
                direction=direction, distance=int(written_instruction.split(" ")[1])
            )
        )
    return instructions


SubmarinePosition = Union[SubmarinePositionWithoutAim, SubmarinePositionWithAim]


def move_submarine(
    instructions: Sequence[Instruction], submarine_position_cls: Callable
) -> SubmarinePosition:
    """Moves a submarine to the terminal location implied by some instructions."""
    submarine_position = submarine_position_cls()
    for instruction in instructions:
        submarine_position = submarine_position.follow_instruction(instruction)

    return submarine_position


def follow_instructions_and_calculate_puzzle_answer(
    written_instructions: str, submarine_position_cls: Callable
) -> int:
    instructions = parse_instructions(written_instructions)
    terminal_submarine_position = move_submarine(instructions, submarine_position_cls)
    return (
        terminal_submarine_position.horizontal_position
        * terminal_submarine_position.depth
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        written_instructions = f.read()

    part_one = follow_instructions_and_calculate_puzzle_answer(
        written_instructions, submarine_position_cls=SubmarinePositionWithoutAim
    )
    part_two = follow_instructions_and_calculate_puzzle_answer(
        written_instructions, submarine_position_cls=SubmarinePositionWithAim
    )
    print(f"Part one: {part_one}")
    print(f"Part one: {part_two}")

