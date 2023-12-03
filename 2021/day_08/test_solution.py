"""Tests for day 8."""

from day_08.solution import (
    Display,
    calculate_total_of_displays,
    calculate_value_of_output,
    count_number_of_digits_with_unique_segment_numbers,
)

_EXAMPLE_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


_SMALLER_EXAMPLE_INPUT = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""


def test_part_one_example_solution_is_recovered():
    assert count_number_of_digits_with_unique_segment_numbers(_EXAMPLE_INPUT) == 26


def test_small_part_two_example():
    assert (
        calculate_value_of_output(Display.from_string(_SMALLER_EXAMPLE_INPUT)) == 5353
    )


def test_larger_part_two_example():
    assert calculate_total_of_displays(_EXAMPLE_INPUT) == 61229
