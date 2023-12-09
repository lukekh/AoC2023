"""AoC :: Day XX"""
from dataclasses import dataclass
import math
import re
import time
from typing import Dict, List, Literal, Set
day = XX


# parse inputs
with open('DayXX/DayXX.in', encoding="utf8") as f:
    inputs = [i[:-1] for i in f.readlines()]


# part one
def part_one():
    """Solution to part one"""
    return 1

# part two
def part_two():
    """Solution to part two"""
    return 2

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one()
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two()
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
