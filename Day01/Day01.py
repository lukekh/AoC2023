"""AoC :: Day 1"""
import time
import re
from typing import List
day = 1


# Parse inputs
with open('Day01/Day01.in', encoding="utf8") as f:
    inputs = [i[:-1] for i in f.readlines()]


# part one
def part_one(args):
    """Solution to part one"""
    pattern = re.compile(r"\d")
    ns = []
    for arg in args:
        ds = pattern.findall(arg)
        # if len(ds) > 1:
        n = int(ds[0] + ds[-1])
        ns.append(n)
    return sum(ns)

# part two
def part_two(args: List[str]):
    """Solution to part two"""
    # We need to map the keys here to their correct digits
    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    word_digits = "|".join(mapping.keys())
    pattern = re.compile(fr"{word_digits}|\d")
    ns = []
    for arg in args:
        # Some numbers look like "oneight" and both count as occurrences of "one" and "eight"
        # This can be fixed by just finding all the instances of "one" and replacing them with "onene", etc
        for key in mapping:
            arg = arg.replace(key, key + key[1:])
        ds = pattern.findall(arg)
        n = int(mapping.get(ds[0], ds[0]) + mapping.get(ds[-1], ds[-1]))
        ns.append(n)
    return sum(ns)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
