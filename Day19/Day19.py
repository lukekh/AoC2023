"""AoC :: Day 19"""
from dataclasses import dataclass
import re
import time
from typing import Dict, Literal
day = 19

# parse inputs
@dataclass
class Rating:
    """stores values for x, m, a, s"""
    x: int
    m: int
    a: int
    s: int
    # regex pattern for parsing
    pattern = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}")

    def __getitem__(self, item: Literal["x", "m", "a", "s"]):
        return getattr(self, item)

    def total(self):
        """return the total"""
        return self.x + self.m + self.a + self.s

    @classmethod
    def parse(cls, string: str):
        """parse a row into a rating"""
        m = cls.pattern.match(string)
        return Rating(*[int(val) for val in m.groups()])

@dataclass
class RatingRange:
    """stores values for x, m, a, s"""
    x: range
    m: range
    a: range
    s: range

    then: str | None

    def __getitem__(self, item: Literal["x", "m", "a", "s"]) -> range:
        return getattr(self, item)

    def __setitem__(self, item: Literal["x", "m", "a", "s"], val: range):
        match item:
            case "x":
                self.x = val
            case "m":
                self.m = val
            case "a":
                self.a = val
            case "s":
                self.s = val

    def __bool__(self):
        return all([self.x, self.m, self.a, self.s])

    def result(self, affects: Literal["x", "m", "a", "s"], r: range, then: str):
        """return a copy of the range but """
        new_range = RatingRange(
            self.x, self.m, self.a, self.s, then
        )
        new_range[affects] = r
        return new_range

    def vol(self):
        """The number of solutions"""
        if self and (self.then == "A"):
            return (
                (self.x.stop - self.x.start)
                * (self.m.stop - self.m.start)
                * (self.a.stop - self.a.start)
                * (self.s.stop - self.s.start)
            )
        return 0

@dataclass
class Rule:
    """a rule within a workflow"""
    symbol: Literal["x", "m", "a", "s"]
    operation: Literal["<", ">"]
    value: int
    then: str

    @staticmethod
    def parse(string: str):
        """parse a rule chunk from Workflow"""
        comparison, then = string.split(":")
        return Rule(comparison[0], comparison[1], int(comparison[2:]), then)

    def __call__(self, rating: Rating):
        match self.operation:
            case "<":
                return self.then if rating[self.symbol] < self.value else None
            case ">":
                return self.then if rating[self.symbol] > self.value else None

    def on_range(self, rating_range: RatingRange):
        """determine the affects of a rule on a rating range and return a list of subranges"""
        start, stop = rating_range[self.symbol].start, rating_range[self.symbol].stop
        match self.operation:
            case "<":
                return (
                    rating_range.result(self.symbol, range(start, min(self.value, stop)), then=self.then),
                    rating_range.result(self.symbol, range(max(self.value, start), stop), then=None),
                )
            case ">":
                return (
                    rating_range.result(self.symbol, range(start, min(self.value + 1, stop)), then=None),
                    rating_range.result(self.symbol, range(max(self.value + 1, start), stop), then=self.then),
                )

    def __str__(self):
        return self.symbol + self.operation + str(self.value) + ":" + self.then


class Workflow:
    """a workflow"""
    workflows: Dict[str, "Workflow"] = {}

    def __init__(self, name: str, rules: list[Rule], end: str):
        self.name = name
        self.rules = rules
        self.end = end

        self.workflows[name] = self

    def __call__(self, rating: Rating) -> bool:
        """Observe the affects of the workflow on the rating"""
        # Run over rules
        for rule in self.rules:
            then = rule(rating)
            if then == "A":
                return True
            if then == "R":
                return False
            if then is not None:
                return self.workflows[then](rating)

        # if all rules have completed
        if self.end == "A":
            return True
        if self.end == "R":
            return False
        if self.end is not None:
            return self.workflows[self.end](rating)

    def apply_to_ranges(self, rating_range: RatingRange) -> list[RatingRange]:
        """Observe the affects of the workflow on a RatingRange"""
        # Init all RatingRange in workflow
        rating_range.then = None
        rating_ranges = [rating_range]

        # Run over all rules in workflow until something exits
        exited = []
        for rule in self.rules:
            # Run over each RatingRange in rating_ranges
            new_ranges = []
            for rr in rating_ranges:
                if rr.then is None:
                    new_ranges.extend(rule.on_range(rr))
                else:
                    exited.append(rr)
            rating_ranges = new_ranges

        for rr in rating_ranges:
            if rr.then is None:
                rr.then = self.end

        return rating_ranges + exited

    @staticmethod
    def parse(string: str):
        """parse a row into a workflow"""
        name, r = string.split(r"{")
        *rules, end = r.split(",")
        return Workflow(
            name,
            [Rule.parse(rule) for rule in rules],
            end[:-1]
        )


with open('Day19/Day19.in', encoding="utf8") as f:
    workflow_rows, rs = f.read().split("\n\n")
    INIT = None
    for row in workflow_rows.split("\n"):
        w = Workflow.parse(row)
        if w.name == "in":
            INIT = w
    RATINGS = [Rating.parse(i) for i in rs[:-1].split("\n")]

if INIT is None:
    raise ValueError("no 'in' workflow in inputs")

# part one
def part_one(init: Workflow, ratings: list[Rating]):
    """Solution to part one"""
    return sum(rating.total() for rating in ratings if init(rating))

# part two
def part_two(init: Workflow):
    """Solution to part two"""
    ranges = [RatingRange(
        x=range(1,4001),
        m=range(1,4001),
        a=range(1,4001),
        s=range(1,4001),
        then=init.name
    )]

    completed: list[RatingRange] = []

    while ranges:
        new_ranges = [
            nr for r in ranges for nr in Workflow.workflows[r.then].apply_to_ranges(r)
        ]
        completed.extend(r for r in new_ranges if r.then in ("A", "R"))
        ranges = [r for r in new_ranges if r.then not in ("A", "R")]

    return sum(r.vol() for r in completed)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(INIT, RATINGS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(INIT)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
