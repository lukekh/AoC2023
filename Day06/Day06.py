"""AoC :: Day 6"""
from dataclasses import dataclass
import time
import re
import math
from typing import List
day = 6


# Parse inputs
@dataclass
class Race:
    """A representation of a race"""
    time: int
    distance: int

    def ways_of_winning(self):
        """The number of ways you can win the race"""
        delta = math.sqrt(self.time ** 2 - 4 * self.distance)
        roots = ((self.time - delta)/2, (self.time + delta)/2)
        return math.ceil(roots[1] - 1) - math.floor(roots[0] + 1) + 1

re_digits = re.compile(r"\d+")

with open('Day06/Day06.in', encoding="utf8") as f:
    times, distances = [re_digits.findall(i.split(":")[1]) for i in f.readlines()]
    RACES = [
        Race(int(t), int(d)) for t, d in zip(times, distances)
    ]
    NEW_RACE = Race(int(''.join(times)), int(''.join(distances)))

# part one
def product(ps: List[int]):
    """Return the product of integers"""
    if len(ps) > 1:
        return ps[0] * product(ps[1:])
    else:
        return ps[0]

def part_one(races: List[Race]):
    """Solution to part one"""
    return product([race.ways_of_winning() for race in races])

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(RACES)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_one([NEW_RACE])
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
