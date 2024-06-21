"""
AoC :: Day 24

Heavy inspiration taken from [this solution](https://github.com/fuglede/adventofcode/blob/master/2023/day24/solutions.py) for part
two. Although my own attempt at the solution should have worked (I think...) rounding errors from floating point solvers and big
numbers caused it to fail.
"""
from dataclasses import dataclass
import re
import time
from itertools import combinations
from z3 import IntVector, Solver
import numpy as np
day = 24

# Regex for parsing
RE_HAIL = re.compile(r"(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*@\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)")

@dataclass
class Hail:
    """A hailstone class which includes a position at t=0 and a velocity"""
    position: np.ndarray
    velocity: np.ndarray

    @staticmethod
    def parse(s: str):
        """parse a string representation of a hailstone"""
        groups = RE_HAIL.match(s).groups()
        assert groups[4] != 0
        return Hail(
            position = np.array(tuple(map(int, groups[:3])), dtype=int),
            velocity = np.array(tuple(map(int, groups[3:])), dtype=int)
        )

# parse inputs
with open('Day24/Day24.in', encoding="utf8") as f:
    inputs = [Hail.parse(i[:-1]) for i in f.readlines()]


# part one
def part_one(hail: list[Hail], min_: int = 200_000_000_000_000, max_: int = 400_000_000_000_000):
    """Solution to part one"""
    result = 0
    for h1, h2 in combinations(hail, 2):
        p1, p2, _ = h1.position
        dp1, dp2, _ = h1.velocity
        q1, q2, _ = h2.position
        dq1, dq2, _ = h2.velocity
        sp = dp2 / dp1
        sq = dq2 / dq1
        # Skip if trajectories are parallel
        if sp == sq:
            continue
        # Solve for (x, y) coords for collision
        x, y = np.linalg.solve([[-sp, 1], [-sq, 1]], [p2 - sp * p1, q2 - sq * q1])
        if (x - p1) / dp1 < 0 or (x - q1) / dq1 < 0:
            continue
        if min_ <= x <= max_ and min_ <= y <= max_:
            result += 1

    return result

# part two
def part_two(hail: list[Hail], MIN: int = 3):
    """Solution to part two"""
    q1, q2, q3, dq1, dq2, dq3 = IntVector("sol", 6)
    # We only need 3 rocks to solve this
    ts = IntVector("t", min(MIN, len(hail)))

    s = Solver()

    for t, h in zip(ts, hail):
        p1, p2, p3 = h.position
        dp1, dp2, dp3 = h.velocity
        s.add(q1 + t * dq1 == p1 + t * dp1)
        s.add(q2 + t * dq2 == p2 + t * dp2)
        s.add(q3 + t * dq3 == p3 + t * dp3)
    s.check()
    m = s.model()

    # sum coords of init position vector
    return sum(m[v].as_long() for v in (q1, q2, q3))

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
