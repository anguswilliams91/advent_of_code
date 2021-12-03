"""Binary diagnostic."""

from __future__ import annotations

from enum import Enum
from typing import NamedTuple, Sequence


class Rates(NamedTuple):
    """Represents the gamma and epsilon rate of a submarine."""

    gamma_rate: int
    epsilon_rate: int

    @classmethod
    def from_codes(cls, binary_codes: str) -> Rates:
        """Calculates the gamma and epsilon rates from given binary codes."""
        gamma_rate, epsilon_rate = cls.calculate_gamma_and_epsilon_rates(
            binary_codes.splitlines()
        )
        return cls(gamma_rate=int(gamma_rate, 2), epsilon_rate=int(epsilon_rate, 2))

    def calculate_gamma_and_epsilon_rates(binary_codes: Sequence[str]) -> Sequence[str]:
        num_codes = len(binary_codes)
        num_zeros = [0] * len(binary_codes[0])
        for code in binary_codes:
            for i, bit in enumerate(code):
                num_zeros[i] += bit == "0"
        gamma_rate = "".join("0" if n > num_codes // 2 else "1" for n in num_zeros)
        epsilon_rate = gamma_rate.translate(str.maketrans("01", "10"))
        return (gamma_rate, epsilon_rate)


class RatingType(Enum):
    OXYGEN_GENERATOR = 1
    CO2_SCRUBBER = 2


class Ratings(NamedTuple):
    """Container for Oxygen generator ratings and CO2 scrubber ratings."""

    oxygen_generator_rating: int
    co2_scrubber_rating: int

    @classmethod
    def from_codes(cls, binary_codes: str) -> Ratings:
        binary_codes = binary_codes.splitlines()
        oxygen_generator_rating = cls.calculate_rating(
            binary_codes, rating_type=RatingType.OXYGEN_GENERATOR
        )
        co2_scrubber_rating = cls.calculate_rating(
            binary_codes, rating_type=RatingType.CO2_SCRUBBER
        )
        return cls(
            oxygen_generator_rating=int(oxygen_generator_rating, 2),
            co2_scrubber_rating=int(co2_scrubber_rating, 2),
        )

    def calculate_rating(
        binary_codes: Sequence[str], rating_type: RatingType, bit_position: int = 0
    ):
        gamma_rate, epsilon_rate = Rates.calculate_gamma_and_epsilon_rates(binary_codes)
        rate = (
            gamma_rate if rating_type is RatingType.OXYGEN_GENERATOR else epsilon_rate
        )
        codes_satisfying_bit_criterion = [
            c for c in binary_codes if c[bit_position] == rate[bit_position]
        ]
        if len(codes_satisfying_bit_criterion) > 1:
            return Ratings.calculate_rating(
                codes_satisfying_bit_criterion,
                rating_type,
                bit_position=bit_position + 1,
            )
        else:
            return codes_satisfying_bit_criterion[0]


def calculate_power_consumption(binary_codes: str) -> int:
    """Calculates the power consumption of the submarine."""
    rates = Rates.from_codes(binary_codes)
    return rates.gamma_rate * rates.epsilon_rate


def calculate_life_support_rating(binary_codes: str) -> int:
    """Calculates the life support rating of the submarine."""
    ratings = Ratings.from_codes(binary_codes)
    return ratings.oxygen_generator_rating * ratings.co2_scrubber_rating


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        binary_codes = f.read()

    print(f"Part one: {calculate_power_consumption(binary_codes)}")
    print(f"Part two: {calculate_life_support_rating(binary_codes)}")
