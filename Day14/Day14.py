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

# HELPER FUNCTION
def hash_grid(grid: dict[int, list[Rock]]):
    """helper function to hash grid"""
    return '\n'.join([''.join(rock.kind for rock in rocks) for _, rocks in grid.items()])

# part one
def part_one(grid: dict[int, list[Rock]]):
    """Solution to part one"""
    new_grid: dict[int, list[Rock]] = {}
    total = 0
    for col, rocks in grid.items():
        load = N
        for rock in sorted(rocks, key=lambda x: x.row):
            match rock.kind:
                case "#":
                    load = N - rock.row
                    new_grid.setdefault(load-1, []).append(Rock("#", col, load-1))
                    load -= 1
                case "O":
                    total += load
                    new_grid.setdefault(load-1, []).append(Rock("O", col, load-1))
                    load -= 1
    return total, new_grid

# part two
def load_no_slide(grid: dict[int, list[Rock]]):
    """Do part one without sliding"""
    total = 0
    for _, rocks in grid.items():
        for rock in rocks:
            match rock.kind:
                case "#":
                    pass
                case "O":
                    total += N - rock.row
    return total

def part_two(grid: dict[int, list[Rock]], n: int = 1_000_000_000):
    """Solution to part two"""
    def cycle(grid: dict[int, list[Rock]]):
        for _ in range(4):
            _, grid = part_one(grid)
        return _, grid

    cache = {}
    i = 0
    cycle_detected = False
    while i < n:
        _, grid = cycle(grid)
        if not cycle_detected:
            s = hash_grid(grid)
            if (s not in cache) and (not cycle_detected):
                cache[s] = i
            elif (s in cache) and (not cycle_detected):
                cycle_length = i - cache[s]
                m = (n - i)//cycle_length
                i += m * cycle_length
                cycle_detected = True
        i += 1
    return load_no_slide(grid)

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
