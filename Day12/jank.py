"""
A defunct attempt at AoC Day 12
"""
from enum import Enum
from dataclasses import dataclass
import re
import time
from typing import List, SupportsIndex
day = 12


# parse inputs
class Condition(Enum):
    """The condition of a spring"""
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"

    def possibly_damaged(self):
        """returns True if condition is DAMAGED (#) or UNKNOWN (?)"""
        return self in (Condition.DAMAGED, Condition.UNKNOWN)

    def possibly_operational(self):
        """returns True if condition is OPERATIONAL (.) or UNKNOWN (?)"""
        return self in (Condition.OPERATIONAL, Condition.UNKNOWN)

    def __bool__(self):
        return self is Condition.DAMAGED


class Conditions(List[Condition]):
    """a row of conditions"""
    def __setitem__(self, __key: SupportsIndex, __value: Condition):
        if __key != -1:
            try:
                super().__setitem__(__key, __value)
            except IndexError:
                pass
        else:
            pass

    def groups(self):
        """find all known DAMAGED sections"""
        buffered = [Condition.OPERATIONAL] + self + [Condition.OPERATIONAL]
        idxs = [i for i, c in enumerate(buffered) if c is Condition.OPERATIONAL]
        return Record([
            length if all(buffered[i+1:j]) else None for i, j in zip(idxs, idxs[1:]) if (length := j - i - 1) and any(buffered[i+1:j])
        ])

    def possible(self, length: int):
        """return the list of possible records given a length"""
        possible: List[Conditions] = []
        buffered = [Condition.OPERATIONAL] + self + [Condition.OPERATIONAL]
        # try:
        #     stop = buffered.index(Condition.OPERATIONAL, min(i for i, c in enumerate(buffered) if c.possibly_damaged()))
        #     buffered = Conditions(buffered[:stop] + [Condition.OPERATIONAL])
        #     print(buffered)
        # except ValueError:
        #     pass
        for idx, condition in enumerate(buffered):
            if condition.possibly_damaged():
                start, *middle, end = buffered[idx-1:idx+length+1]
                if (
                    all(c.possibly_damaged() for c in middle) and
                    (len(middle) == length) and
                    start.possibly_operational() and
                    end.possibly_operational()
                ):
                    p = Conditions(self.copy())
                    del p[: idx+length]
                    possible.append(p)
        print(possible)
        return possible

    def __repr__(self):
        return "{" + "".join(c.value for c in self) + "}"

    def __str__(self):
        return "".join(c.value for c in self)


class Record(List[int | None]):
    """A record that supports valid comparisons"""
    def __contains__(self, other: "Record"):
        idx = 0
        for n in other:
            if n is not None:
                try:
                    idx = self.index(n, idx) + 1
                except ValueError:
                    return False
            else:
                idx += 1
        return True


@dataclass
class Row:
    """The conditions of a row of springs and a record"""
    conditions: Conditions
    record: Record
    # Globals
    RE_SOLVED = re.compile(r"\.#+\.")

    def valid(self):
        """check some basic conditions to see if it is aligned with record"""
        string = str(self.conditions)
        if string.count("#") + string.count("?") >= sum(self.record):
            return self.conditions.groups() in self.record
        return False

    def solve_next(self):
        """Solve for the next record condition"""
        # Some basic error handling
        new_record = Record(self.record.copy())
        length = new_record.pop(0)
        rows = [
            Row(condition, new_record) for condition in self.conditions.possible(length)
        ]
        return [row for row in rows if row.valid()]



def parse(row: str):
    """parse a row"""
    conditions, record = row.split(" ")
    return Row(
        conditions=Conditions([Condition(char) for char in conditions]),
        record=Record([int(i) for i in record.split(",")])
    )

with open('Day12/Day12.in', encoding="utf8") as f:
    ROWS = [parse(row) for row in f.readlines()]
    # for i, r in enumerate(ROWS):
    #     assert r.valid(), f"{i}: {r}"
    # # unit tests
    # test1 = parse("?????#? 6")
    # print(test1)
    # print(test1.valid())
    # print(test1.conditions.possible(6))
    # print(test1.solve_next())
    # # # print(test1(0))
    # # assert test1.valid(), "test is invalid"
    # assert False

# part one
def part_one(rows: List[Row]):
    """Solution to part one"""
    def recurse(row: Row, lvl=0):
        print()
        print(" " * lvl * 4, row)
        print(" " * lvl * 4, row.record, bool(row.record))
        if row.record:
            # print(" " * lvl * 4, row.conditions.possible(row.record[0]))
            return sum(recurse(new_row, lvl+1) for new_row in row.solve_next())
        print(" " * lvl * 4, "terminal")
        return 1
    total = 0
    for row in rows:
        print(row)
        val = recurse(row)
        total += val
        print(f"val: {val}")
        print("---")
    return total

# part two
def part_two():
    """Solution to part two"""
    return 2

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
    a2 = part_two()
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
