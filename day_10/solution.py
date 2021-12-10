"""10. Syntax scoring."""

from dataclasses import dataclass
from statistics import median

_CORRUPTION_POINTS_BY_BRACE_TYPE = {")": 3, "]": 57, "}": 1197, ">": 25137}
_COMPLETION_POINTS_BY_BRACE_TYPE = {"(": 1, "[": 2, "{": 3, "<": 4}
_BRACES = {"(": ")", "[": "]", "{": "}", "<": ">"}


@dataclass
class Scores:
    syntax_score: int = 0
    completion_score: int = 0


def calculate_scores_of_line(line: str) -> int:
    """Calculates the syntax and completion scores of a line in a navigation subsystem."""
    scores = Scores()
    brace_queue = []
    for brace in line:
        if brace in _BRACES:
            brace_queue.append(brace)
        else:
            if brace_queue and brace == _BRACES[brace_queue[-1]]:
                brace_queue.pop()
            else:
                scores.syntax_score = _CORRUPTION_POINTS_BY_BRACE_TYPE[brace]
                return scores

    for brace in reversed(brace_queue):
        scores.completion_score = (
            scores.completion_score * 5 + _COMPLETION_POINTS_BY_BRACE_TYPE[brace]
        )
    return scores


def calculate_syntax_score_of_navigation_subsystem(navigation_subsystem: str) -> int:
    """Calculates the overall syntax score of a navigation subsystem."""
    return sum(
        calculate_scores_of_line(line).syntax_score
        for line in navigation_subsystem.splitlines()
    )


def calculate_completion_score_of_navigation_subsystem(
    navigation_subsystem: str
) -> int:
    """Calculates the overall completion score of a navigation subsystem."""
    return median(
        s for line in navigation_subsystem.splitlines()
        if (s := calculate_scores_of_line(line).completion_score) > 0
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        navigation_subsystem = f.read()

    part_one = calculate_syntax_score_of_navigation_subsystem(navigation_subsystem)
    part_two = calculate_completion_score_of_navigation_subsystem(navigation_subsystem)
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")

