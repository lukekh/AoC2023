"""
AoC :: Day 12

I had to get help with this one. I was going in a direction that wasn't working,
so turned to the subreddit for help. I saw [this comment](https://www.reddit.com/r/adventofcode/comments/18ge41g/comment/kd93dvp/)
which took me to [this code](https://github.com/clrfl/AdventOfCode2023/tree/dde3f76117127565c35c055ddcaa5d9aa4109097/12)
which is where I got the code for the automata function below.
"""
from enum import Enum
from dataclasses import dataclass
import time
from typing import List
day = 12

class Condition(Enum):
    """The condition of a spring"""
    OPERATIONAL = "."
    DAMAGED     = "#"
    UNKNOWN     = "?"

@dataclass
class Row:
    """The conditions of a row of springs and a record"""
    conditions: list[Condition]
    record: list[int]

    def unfold(self):
        """unfold the record"""
        conditions = self.conditions.copy()
        for _ in range(4):
            conditions += [Condition.UNKNOWN] + self.conditions
        return Row(conditions, self.record * 5)

def parse(row: str):
    """parse a row"""
    conditions, record = row.split(" ")
    return Row(
        conditions = [Condition(c) for c in conditions],
        record = [int(i) for i in record.split(",")]
    )

with open('Day12/Day12.in', encoding="utf8") as f:
    ROWS = [parse(row) for row in f.readlines()]

# part one
def automata(row: Row):
    """use automata theory to get total combinations"""
    # These lay out the state indices that correspond to operational conditions
    # as per the record
    t = 0
    operational = [0] + [(t:= t + int(n) + 1) for n in row.record]
    N = operational[-1]

    # Init states
    # We begin with a single active solution at the root state 0
    states_dict = {0: 1}
    # Iterate over the condition string character by character
    # Add a trailing OPERATIONAL as a terminal state
    for char in row.conditions + [Condition.OPERATIONAL]:
        new_dict = {}
        for state, val in states_dict.items():
            match char:
                case Condition.UNKNOWN:
                    new_dict[state + 1] = new_dict.get(state + 1, 0) + val
                    if state in operational:
                        new_dict[state] = new_dict.get(state, 0) + val
                case Condition.OPERATIONAL:
                    if state + 1 in operational:
                        new_dict[state + 1] = new_dict.get(state + 1, 0) + val
                    if state in operational:
                        new_dict[state] = new_dict.get(state, 0) + val
                case Condition.DAMAGED:
                    if state + 1 not in operational:
                        new_dict[state + 1] = new_dict.get(state + 1, 0) + val
        states_dict = new_dict
    return states_dict.get(N, 0)

def part_one(rows: List[Row]):
    """Solution to part one"""
    return sum(automata(row) for row in rows)

# part two
def part_two(rows: List[Row]):
    """Solution to part two"""
    return sum(automata(row.unfold()) for row in rows)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(ROWS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(ROWS)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
