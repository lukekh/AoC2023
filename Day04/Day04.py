"""AoC :: Day 4"""
from dataclasses import dataclass
import re
import time
from typing import List, Set
day = 4


# Parse inputs
@dataclass
class Ticket:
    """A representation of a ticket"""
    win: Set[int]
    has: Set[int]

    @property
    def points(self):
        """The number of points from part one"""
        return int(2**(len(self.win & self.has) - 1))

    def matches(self):
        """The number of winning matches on the card"""
        return len(self.win & self.has)

re_digits = re.compile(r"\d+")
def parse(s: str):
    """Turn a string into a Ticket dataclass"""
    win, has = s.split(":")[1].split("|")
    return Ticket({int(n) for n in re_digits.findall(win)}, {int(n) for n in re_digits.findall(has)})

with open('Day04/Day04.in', encoding="utf8") as f:
    inputs = [parse(i) for i in f.readlines()]


# part one
def part_one(tickets: List[Ticket]):
    """Solution to part one"""
    return sum(ticket.points for ticket in tickets)

# part two
def part_two(tickets: List[Ticket]):
    """Solution to part two"""
    copies = {i: 1 for i in range(len(tickets))}
    for i, ticket in enumerate(tickets):
        n = ticket.matches()
        for j in range(1, n+1):
            copies[i+j] += copies[i]
    return sum(copies.values())

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
