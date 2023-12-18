"""AoC :: Day 14"""
from dataclasses import dataclass
import time
from typing import Literal
day = 14


# parse inputs
@dataclass
class Rock:
    """represents a rock on a grid"""
    kind: Literal["#", "O"]
    row: int
    col: int

with open('Day14/Day14.in', encoding="utf8") as f:
    GRID: dict[int, list[Rock]] = {}
    N = 0 # Prevents N being unbound
    for r, string in enumerate(f.readlines()):
        N = r + 1
        for c, char in enumerate(string):
            if char in ("#", "O"):
                GRID.setdefault(c, []).append(Rock(char, r, c))

# part one
def part_one(grid: dict[int, list[Rock]]):
    """Solution to part one"""
    new_grid: dict[int, list[Rock]] = {}
    total = 0
    for col, rocks in grid.items():
        load = N
        for rock in rocks:
            match rock.kind:
                case "#":
                    new_grid.setdefault(col, []).append(Rock("O", col, N - rock.row))
                    load = N - rock.row - 1
                case "O":
                    total += load
                    new_grid.setdefault(col, []).append(Rock("O", col, load))
                    load -= 1
    return total, new_grid

# part two
def part_two(grid: dict[int, list[Rock]], n: int = 1_000_000_000):
    """Solution to part two"""
    def cycle(grid: dict[int, list[Rock]]):
        for _ in range(4):
            total, grid = part_one(grid)
        return total, grid

    for i in range(2):
        total, grid = cycle(grid)
        print(f"cycle {i}: {total}")
    return 1

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1, _ = part_one(GRID)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(GRID)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
