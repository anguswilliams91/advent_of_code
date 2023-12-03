"""7. The treachery of whales."""

from enum import Enum

from statistics import mean, median


def find_fuel_spend_using_simple_rule(horizontal_positions: str) -> int:
    """Finds the minimum fuel spend required to align the crab submarines."""
    crab_positions = [int(p) for p in horizontal_positions.split(",")]
    median_position = median(crab_positions)
    return int(sum(abs(p - median_position) for p in crab_positions))


def find_fuel_spend_using_complex_rule(horizontal_positions: str) -> int:
    """Same as above but for the more complex rule.
    
    The constraint in part 2 leads to:
    
    Fuel = Sum_i[ 1/2 (p - xi)^2 + 1/2 |p - xi| ]

    where xi is position of the ith crab, and p is the optimal location for the crabs
    to align. Differentiating this and rearranging gives:
    
    p = Sum_i[xi] / N - Sum_i[ Sign[p - xi]  / 2N]

    The first term on the RHS is the mean of the crab positions, and the second term
    is between -1/2 and 1/2. So p must satisfy

    Mean[xi] - 1 / 2 <= p <= Mean[xi] + 1/2

    [n.b. I derived most of this but missed the last step to get the tighter bound!]

    """
    crab_positions = [int(p) for p in horizontal_positions.split(",")]
    fuel_used = lambda p: sum(0.5 * ((p - c) ** 2 + abs(p - c)) for c in crab_positions)
    mean_crab_position = mean(crab_positions)
    p_candidates = range(
        int(mean_crab_position - 1 / 2), int(mean_crab_position + 1 / 2) + 1
    )
    return int(min(map(fuel_used, p_candidates)))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        horizontal_positions = f.read()

    print(f"Part one: {find_fuel_spend_using_simple_rule(horizontal_positions)}")
    print(f"Part two: {find_fuel_spend_using_complex_rule(horizontal_positions)}")

