"""Day 5: If You Give A Seed A Fertilizer"""

from __future__ import annotations

import bisect
import dataclasses


@dataclasses.dataclass
class Map:
    dest_start: list[int]
    source_start: list[int]
    range_size: list[int]

    @classmethod
    def from_string(cls, map_text: str) -> Map:
        """Makes a map from its string representation."""
        dest_starts = []
        source_starts = []
        range_sizes = []
        for part in map_text.split(":")[1].strip().splitlines():
            dest_start, source_start, range_size = [int(p) for p in part.split()]
            dest_starts.append(dest_start)
            source_starts.append(source_start)
            range_sizes.append(range_size)
        # Sorts the three lists so that they are in the order that corresponds to
        # source_starts being in ascending order.
        sorted_combined = sorted(
            list(zip(dest_starts, source_starts, range_sizes)), key=lambda x: x[1]
        )
        return cls(
            dest_start=[e[0] for e in sorted_combined],
            source_start=[e[1] for e in sorted_combined],
            range_size=[e[2] for e in sorted_combined],
        )

    def __getitem__(self, source: int) -> int:
        """Gets a destination value from a source value."""
        i = bisect.bisect_left(self.source_start, source)
        if i == len(self.source_start):
            # Given source value is larger than the largest start.
            j = i - 1
        elif source - self.source_start[i] == 0:
            # Given source value is equal to a start.
            j = i
        else:
            # Given source value is between two start values, so we should choose
            # the left one.
            j = i - 1

        if 0 < (diff := source - self.source_start[j]) <= self.range_size[j]:
            return self.dest_start[j] + diff

        # If the given source value doesn't lie in any of the provided map ranges, then
        # it maps to itself.
        return source


@dataclasses.dataclass
class Almanac:
    seeds: list[int]
    seed_to_soil: Map
    soil_to_fertilizer: Map
    fertilizer_to_water: Map
    water_to_light: Map
    light_to_temperature: Map
    temperature_to_humidity: Map
    humidity_to_location: Map

    @classmethod
    def from_string(cls, almanac_text) -> Almanac:
        """Makes an Almanac from its string representation."""
        parts = almanac_text.split("\n\n")
        return cls(
            seeds=[int(p) for p in parts[0].split(":")[1].strip().split()],
            seed_to_soil=Map.from_string(parts[1]),
            soil_to_fertilizer=Map.from_string(parts[2]),
            fertilizer_to_water=Map.from_string(parts[3]),
            water_to_light=Map.from_string(parts[4]),
            light_to_temperature=Map.from_string(parts[5]),
            temperature_to_humidity=Map.from_string(parts[6]),
            humidity_to_location=Map.from_string(parts[7]),
        )

    def __getitem__(self, seed: int) -> int:
        """Maps a seed to its location given the chain of maps."""
        soil = self.seed_to_soil[seed]
        fertilizer = self.soil_to_fertilizer[soil]
        water = self.fertilizer_to_water[fertilizer]
        light = self.water_to_light[water]
        temperature = self.light_to_temperature[light]
        humidity = self.temperature_to_humidity[temperature]
        return self.humidity_to_location[humidity]


def solve(almanac_text: str) -> int:
    """Finds the lowest location number given an almanac."""
    almanac = Almanac.from_string(almanac_text)
    return min(almanac[s] for s in almanac.seeds)


def main():
    with open("input.txt", "r") as f:
        almanac_text = f.read()

    lowest_location = solve(almanac_text)

    print("Part 1: ", lowest_location)


if __name__ == "__main__":
    main()
