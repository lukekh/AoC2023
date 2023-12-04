"""AoC :: Day 3"""
from dataclasses import dataclass
import time
import re
from typing import Set, Tuple
day = 3


# Parse inputs
@dataclass
class Number:
    """a number and its range of coordinates (given by a row and its start and end column)"""
    n: int
    row: int
    start: int
    end: int
    # This caches the coord calculation so it isn't repeated unnecessarily
    _surrounding_coordinates: Tuple[int, int] = None

    @property
    def surrounding_coordinates(self):
        """return all the """
        if self._surrounding_coordinates is None:
            self._surrounding_coordinates = {(r, c) for r in range(self.row-1, self.row+2) for c in range(self.start-1, self.end+2)}
        return self._surrounding_coordinates


    def __hash__(self):
        return hash((self.n, self.row, self.start, self.end, "Number"))

@dataclass
class Symbol:
    """A symbol and its coordinate"""
    char: str
    row: int
    col: int

    def __hash__(self):
        return hash((self.char, self.row, self.col, "Symbol"))

re_number = re.compile(r"^\d+")
DIGITS = [str(i) for i in range(10)]
re_symbol = re.compile(r"^[^\d\.]")

def parse(s: str, row: int):
    """parse inputs"""
    numbers = []
    symbols = []
    acc = ""

    for i, char in enumerate(s):
        if char in (".", "\n"):
            if acc:
                numbers.append(Number(int(acc), row, i-len(acc), i-1))
            acc = ""
        elif char in DIGITS:
            acc += char
        else:
            if acc:
                numbers.append(Number(int(acc), row, i-len(acc), i-1))
            symbols.append(Symbol(char, row, i))
            acc = ""
    return set(numbers), set(symbols)


with open('Day03/Day03.in', encoding="utf8") as f:
    NUMBERS: Set[Number] = set()
    SYMBOLS: Set[Symbol] = set()
    for r, line in enumerate(f.readlines()):
        matches, syms = parse(line, r)
        NUMBERS |= matches
        SYMBOLS |= syms


# part one
def part_one(numbers: Set[Number], symbols: Set[Symbol]):
    """Solution to part one"""
    coords = {(symbol.row, symbol.col) for symbol in symbols}

    def part_number_check(number: Number, coords: Set[Tuple[int, int]]=coords):
        """Return whether the number is a part number based on the coordinates of symbols"""
        return bool(number.surrounding_coordinates & coords)

    part_numbers = {number for number in numbers if part_number_check(number, coords)}
    # Return part numbers for an easier part two
    return sum(number.n for number in part_numbers), part_numbers

# part two
def part_two(part_numbers: Set[Number], symbols: Set[Symbol]):
    """Solution to part two"""
    def gear_ratio(symbol: Symbol, part_numbers: Set[Number] = part_numbers):
        """Calculate the gear ratio for a symbol and return 0 if it isn't a gear"""
        if symbol.char == "*":
            gears = [number for number in part_numbers if (symbol.row, symbol.col) in number.surrounding_coordinates]
            if len(gears) == 2:
                return gears[0].n * gears[1].n
        return 0

    return sum(gear_ratio(symbol) for symbol in symbols)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1, part_numbers = part_one(NUMBERS, SYMBOLS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(part_numbers, SYMBOLS)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
