"""Day 6: Wait For It"""
from __future__ import annotations

import dataclasses
import math


@dataclasses.dataclass
class RaceHistory:
    time: list[int]
    distance: list[int]

    @classmethod
    def from_string(cls, paper: str, remove_whitespace: bool) -> RaceHistory:
        """Returns a race history from the information on the piece of paper."""
        lines = paper.splitlines()
        if remove_whitespace:
            return cls(
                time=[int(lines[0].split(":")[1].strip().replace(" ", ""))],
                distance=[int(lines[1].split(":")[1].strip().replace(" ", ""))],
            )
        return cls(
            time=[int(t) for t in lines[0].split(":")[1].strip().split()],
            distance=[int(d) for d in lines[1].split(":")[1].strip().split()],
        )


def solve(race_history: RaceHistory) -> int:
    """Calculates the product of the number of ways the record can be broken per race."""
    # If Tb is the time spent holding the button, and Tr is the total race time,
    # then the distance travelled is:
    # D = Tb * (Tr - Tb)
    # So to beat the record distance Dr we must have:
    # Tb * (Tr - Tb) > Dr
    # This produces a quadratic inequality with solution
    # Tl = 1/2 * (Tr - sqrt(Tr^2 - 4Dr)) < Tb < Tu = 1/2 * (Tr + sqrt(Tr^2 - 4Dr))
    # We then need to count the number of integers inside this range, which is the same
    # as the number of ways to beat the record.
    # If Floor(Tu) is not an integer, then the number of integers between these two
    # numbers is Floor(Tu) - Floor(Tl).
    # If Tu is an integer, then Floor(Tu) is no longer a solution because it is equal
    # to the right side of the interval, meaning we have to subtract one:
    # Floor(Tu) - Floor(Tl) - 1
    answer = 1
    for t, d in zip(race_history.time, race_history.distance):
        lo = math.floor(0.5 * (t - math.sqrt(t**2 - 4 * d)))
        right_limit = 0.5 * (t + math.sqrt(t**2 - 4 * d))
        hi = math.floor(right_limit)
        answer *= hi - lo - (int(right_limit) == right_limit)
    return answer


def main():
    with open("input.txt", "r") as f:
        paper = f.read()

    part_one_races = RaceHistory.from_string(paper, remove_whitespace=False)
    part_two_race = RaceHistory.from_string(paper, remove_whitespace=True)
    print("Part 1: ", solve(part_one_races))
    print("Part 2: ", solve(part_two_race))


if __name__ == "__main__":
    main()
