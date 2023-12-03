"""Day 1: Trebuchet?!"""

import re

from typing import Sequence

_DIGIT_RE = re.compile(r"(\d)")
_WORD_OR_DIGIT_RE = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")
_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def to_digit(digit_or_word: str) -> str:
    """Converts a string that is either a number or word into a number."""
    if len(digit_or_word) == 1:
        return digit_or_word
    else:
        return str(_WORDS.index(digit_or_word) + 1)


def get_calibration_value(text: str, pattern: re.Pattern) -> int:
    """Finds all digits in a string and concatenates them in to a number."""
    matches = re.findall(pattern, text)
    digits = [to_digit(m) for m in (matches[0], matches[-1])]
    return int("".join(digits))


def sum_calibration_values(document: Sequence[str], pattern: re.Pattern) -> int:
    """Gets all the two digit numbers and sums them."""
    return sum(get_calibration_value(text, pattern) for text in document)


def main():
    with open("input.txt", "r") as f:
        document = f.readlines()

    print("Part one: ", sum_calibration_values(document, _DIGIT_RE))
    print("Part two: ", sum_calibration_values(document, _WORD_OR_DIGIT_RE))


if __name__ == "__main__":
    main()
