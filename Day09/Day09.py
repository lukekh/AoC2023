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


# part one & two
def part_one(histories: List[List[int]]):
    """Solution to part one (plus we sneak in part two)"""
    def recurse(history: List[int], acc_end: int = 0, acc_start: int = 0, alt: bool = False):
        """
        recursively find deltas between history elements until they're all zero
        
        this is complicated to simultaneously calculate part two, bordering on unreadable.
        we simply need to sum the acc_end terms for part one.
        for part two, it's the same as part one on the reversed list of inputs, but
        the deltas accrue a negative sign at each step so it alternates adding and subtracting
        the delta terms.
        """
        if any(history):
            return recurse(
                [ni - nj for ni, nj in zip(history[1:], history)],
                acc_end + history[-1],
                acc_start - history[0] if alt else acc_start + history[0],
                not alt
            )
        # any(history) will be false if each element is 0, so return accumulator
        return acc_end, acc_start

    ends, starts = zip(*map(recurse, histories))

    return sum(ends), sum(starts)


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1, a2 = part_one(HISTORIES)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    # Save double handling by calculating it in part one
    t2 = 0
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
