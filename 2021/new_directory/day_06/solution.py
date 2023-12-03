"""6. Lanternfish."""

from __future__ import annotations

from collections import Counter, defaultdict
import copy
from typing import Mapping


LanternFishSchool: Mapping[int, int]


def evolve_school(school: LanternFishSchool, days: int) -> LanternFishSchool:
    """Evolves the state of a lanternfish by a given number of days."""
    for _ in range(days):
        new_school = copy.copy(school)
        for timer_value, num_fish in school.items():
            if num_fish > 0:
                if timer_value == 0:
                    new_school[0] -= num_fish
                    new_school[6] += num_fish
                    new_school[8] += num_fish
                else:
                    new_school[timer_value] -= num_fish
                    new_school[timer_value - 1] += num_fish
        school = new_school

    return school


def find_total_lanternfish(initial_school: str, days: int) -> int:
    """Finds the total number of lanternfish after a given number of days."""
    initial_school = defaultdict(
        int, Counter(int(n) for n in initial_school.split(","))
    )
    school = evolve_school(initial_school, days)
    return sum(school.values())


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        initial_school = f.read()

    print(f"Part one: {find_total_lanternfish(initial_school, days=80)}")
    print(f"Part one: {find_total_lanternfish(initial_school, days=256)}")

