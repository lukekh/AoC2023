"""AoC :: Day 19"""
from dataclasses import dataclass
import math
import re
import time
from typing import Dict, List, Literal, Set
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

    def __call__(self, rating: Rating):
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
    workflow_rows, ratings = f.read().split("\n\n")
    INIT = None
    for row in workflow_rows.split("\n"):
        w = Workflow.parse(row)
        if w.name == "in":
            INIT = w
    RATINGS = [Rating.parse(i) for i in ratings[:-1].split("\n")]

if INIT is None:
    raise ValueError("no 'in' workflow in inputs")

# part one
def part_one(init: Workflow, ratings: list[Rating]):
    """Solution to part one"""
    return sum(rating.total() for rating in ratings if init(rating))

# part two
def part_two(init: Workflow):
    """Solution to part two"""
    def size_range_dict(d: dict[str, range]):
        p = 1
        for r in d.values():
            p *= max(r.stop - r.start, 0)
        return p

    def recurse(workflow: Workflow, ranges = None, accepted: int = 0, indent = 0):
        """recursively solve"""
        # init
        if ranges is None:
            ranges = {
                "x" : range(1, 4001),
                "m" : range(1, 4001),
                "a" : range(1, 4001),
                "s" : range(1, 4001)
            }
        # apply rules
        pad = " " * 4 * indent if indent else ""
        print(pad + f"start workflow: {workflow.name}", ranges)
        pad = " " * 4 * (indent+1) if indent else ""
        for rule in workflow.rules:
            affected_range = ranges[rule.symbol]
            match rule.operation:
                case "<":
                    if affected_range.start < rule.value:
                        # split
                        left = ranges.copy()
                        left[rule.symbol] = range(affected_range.start, min(rule.value, affected_range.stop))
                        if rule.then == "A":
                            print(pad + f"accepted via rule: {rule},", left)
                            accepted += size_range_dict(left)
                        elif rule.then == "R":
                            print(pad + f"rejected via rule: {rule},", left)
                            pass
                        else:
                            accepted += recurse(Workflow.workflows[rule.then], left, accepted=accepted, indent=indent + 1)
                        # shrink right
                        if rule.value < affected_range.stop:
                            ranges[rule.symbol] = range(rule.value, affected_range.stop)
                            print(pad + "remaining ranges:", ranges)
                        else:
                            print(pad + "no remaining ranges after rule")
                            return accepted
                case ">":
                    if affected_range.stop >= rule.value:
                        right = ranges.copy()
                        right[rule.symbol] = range(max(rule.value, affected_range.start), affected_range.stop)
                        if rule.then == "A":
                            print(pad + f"accepted via rule: {rule},", right)
                            accepted += size_range_dict(right)
                        elif rule.then == "R":
                            print(pad + f"rejected via rule: {rule},", right)
                            pass
                        else:
                            accepted += recurse(Workflow.workflows[rule.then], right, accepted=accepted, indent=indent + 1)
                        if affected_range.start < rule.value:
                            ranges[rule.symbol] = range(affected_range.start, rule.value)
                            print(pad + "remaining ranges:", ranges)
                        else:
                            print(pad + "no remaining ranges after rule")
                            return accepted
        match workflow.end:
            case "A":
                print(pad + "end", workflow.name, "accepted", ranges)
                return accepted + size_range_dict(ranges)
            case "R":
                print(pad + "end", workflow.name, "rejected", ranges)
                return accepted
            case _:
                return recurse(Workflow.workflows[workflow.end], ranges, accepted=accepted, indent=indent + 1)
    return recurse(init)

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
