"""AoC :: Day 11"""
from dataclasses import dataclass
import time
from typing import List, Set
day = 11


# parse inputs
@dataclass
class Galaxy:
    """Represent a Galaxy in the image"""
    row: int
    col: int

    def distance(self, other: "Galaxy", scaling_factor: int = 1):
        """the expanded distance between galaxies"""
        # Expansion along rows
        row_exp_start, row_exp_end = sorted([self.row, other.row])
        row_exp = len(set(range(row_exp_start, row_exp_end + 1)) - ROWS) * (scaling_factor - 1)
        # Expansion along cols
        col_exp_start, col_exp_end = sorted([self.col, other.col])
        col_exp = len(set(range(col_exp_start, col_exp_end + 1)) - COLS) * (scaling_factor - 1)
        return abs(self.row - other.row) + abs(self.col - other.col) + row_exp + col_exp

def parse(row: int, string: str) -> Set[Galaxy]:
    """Parse string into a set of Galaxies"""
    return [Galaxy(row, col) for col, char in enumerate(string) if char == "#"]

GALAXIES: List[Galaxy] = []
with open('Day11/Day11.in', encoding="utf8") as f:
    for r, s in enumerate(f.readlines()):
        GALAXIES += parse(r, s)

# Populate the rows and columns
ROWS, COLS = {g.row for g in GALAXIES}, {g.col for g in GALAXIES}

# part one
def part_one(galaxies: List[Galaxy], scaling_factor: int = 1):
    """Solution to part one"""
    return sum(
        g1.distance(g2, scaling_factor) for i, g1 in enumerate(galaxies) for g2 in galaxies[i+1:]
    )

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(GALAXIES)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_one(GALAXIES, scaling_factor = 1_000_000)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
