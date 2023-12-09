"""AoC :: Day 9"""
import time
from typing import List
day = 9


# parse inputs
def parse(row: str):
    """parse a history row into a list of integers"""
    return [int(n) for n in row.split(" ")]
with open('Day09/Day09.in', encoding="utf8") as f:
    HISTORIES = [parse(i[:-1]) for i in f.readlines()]


# part one
def part_one(histories: List[List[int]]):
    """Solution to part one"""
    def recurse(history: List[int], acc: int = 0):
        """
        recursively find deltas between history elements until they're all zero
        accumulating the last element of the history at each step
        """
        if any(history):
            return recurse([ni - nj for ni, nj in zip(history[1:], history)], acc + history[-1])
        # any(history) will be false if each element is 0, so return accumulator
        return acc

    return sum(recurse(h) for h in histories)


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(HISTORIES)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_one([h[::-1] for h in HISTORIES])
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
