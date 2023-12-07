"""AoC :: Day 5"""
from dataclasses import dataclass
import time
from typing import Dict, List
day = 5


# Parse inputs
@dataclass
class Conversion:
    """A representation of a conversion within a map"""
    destination: int
    source: int
    range: int

@dataclass
class Map:
    """A representation of a map"""
    name: str
    conversions: List[Conversion]
    # dict maps from source to Conversion
    _dict: Dict[int, Conversion] = None

    def _to_dict(self):
        if self._dict is None:
            d = {}
            for conversion in self.conversions:
                d[conversion.source] = conversion
            self._dict = d

    def get_maps(self, source: int, r: int):
        """get the maps relevant to a source and range"""
        return sorted(
            [c for c in self.conversions if (c.source <= source + r) and (source <= c.source + c.range)],
            key=lambda conversion: conversion.source
        )

    def __getitem__(self, item: int):
        if not self._dict:
            self._to_dict()
        try:
            _, M = max((k, m) for k, m in self._dict.items() if k <= item)
        except ValueError:
            return item
        if (delta := item - M.source) < M.range:
            return M.destination + (delta)
        else:
            return item



def parse(title: str, numbers: str):
    """parse a map into a title and its array of conversions"""
    array = [Conversion(*[int(n) for n in row.split(" ")]) for row in numbers.strip().split("\n")]
    return Map(title, array)

with open('Day05/Day05.in', encoding="utf8") as f:
    SEEDS, *MAPS = f.read().split("\n\n")
    SEEDS = [int(i) for i in SEEDS.split(" ")[1:]]
    MAPS = [
        parse(*m.split(":")) for m in MAPS
    ]


# part one
def part_one(seeds: List[int], maps: List[Map]):
    """Solution to part one"""
    def location(seed: int, maps: List[Map]=maps):
        """Use the Map __getitem__ to concisely handle this logic"""
        for m in maps:
            seed = m[seed]
        return seed

    return min(location(seed) for seed in seeds)

# part two
def part_two(seeds: List[int], maps: List[Map]):
    """Solution to part two"""
    # Re-interpret seeds as ranges
    seed_ranges = list(zip(seeds[0::2], seeds[1::2]))

    def recursive_exploration(source: int, r: int, maps: List[Map]):
        """Recursively figure out where the range is sent to"""
        # If we haven't gone through all the maps, continue breaking them apart
        if maps:
            M = maps[0]
            # Get the maps that will affect this range from source -> source + r - 1
            conversions = M.get_maps(source, r)
            # Init some vars for iteratively finding where to explore next
            new_explorations = []
            new_source = source
            # For each relevant conversion, figure out how it breaks apart the current range
            # (Note: conversions is sorted by conversion.source)
            for conversion in conversions:
                if new_source >= source + r - 1:
                    break
                # These are the possible breaks
                sections = [
                    (new_source, max(new_source, conversion.source) - 1),
                    (max(new_source, conversion.source), min(source + r, conversion.source + conversion.range) - 1),
                ]
                new_source = min(source + r, conversion.source + conversion.range)
                # Check each new interval has positive length
                for section in sections:
                    if section[0] <= section[1]:
                        new_explorations.append((section[0], section[1] - section[0] + 1))
            # Append on remainder if there is any in the range
            if new_source <= source + r - 1:
                new_explorations.append((new_source, (source + r + 1) - new_source - 1))
            # Recurse
            return min(recursive_exploration(M[new_s], new_r, maps[1:]) for new_s, new_r in new_explorations)
        else:
            # Return the source if there are no mappings, as this would be the minimum value possible in this range
            return source

    return min(recursive_exploration(s, r, maps) for s, r in seed_ranges)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(SEEDS, MAPS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(SEEDS, MAPS)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
