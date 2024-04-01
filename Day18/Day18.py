"""AoC :: Day 18"""
from dataclasses import dataclass
from enum import Enum
import time
day = 18


# parse inputs
class Direction(Enum):
    """a cardinal direction"""
    U = 1j
    L = -1+0j
    D = -1j
    R = 1 + 0j

    def __mul__(self, other: int):
        return self.value * other

@dataclass
class Instruction:
    """an instruction including a direction, number of steps and a colour code"""
    direction: Direction
    steps: int
    code: str
    direction_decode = {
        "0": Direction.R,
        "1": Direction.D,
        "2": Direction.L,
        "3": Direction.U
    }

    @property
    def vector(self):
        """The vector of travel"""
        return self.direction * self.steps

    @staticmethod
    def parse(string: str):
        """parse a row into an instruction"""
        d, n, code = string.split(" ")
        return Instruction(Direction[d], int(n), code[2:-2])

    def decode(self):
        """decode for part two"""
        return Instruction(self.direction_decode[self.code[-1]], int(self.code[:-1], 16), self.code)


with open('Day18/Day18.in', encoding="utf8") as f:
    INSTRUCTIONS = [Instruction.parse(i) for i in f.readlines()]


# part one
def determinant(p1: complex, p2: complex):
    """return the determinant as per the shoelace formula"""
    return (p1.real * p2.imag) - (p1.imag * p2.real)

def part_one(instructions: list[Instruction]):
    """
    Solution to part one
    
    Basically a direct copy from Day10
    """
    # init
    position = 0+0j
    area = 0
    perimeter = 0

    for instruction in instructions:
        v = instruction.vector
        area += determinant(position, position + v)
        perimeter += instruction.steps
        position += instruction.vector
    area = abs(area) // 2
    return int(area + perimeter//2 + 1)

# part two
def part_two(instructions: list[Instruction]):
    """Solution to part two"""
    # init
    position = 0+0j
    area = 0
    perimeter = 0

    for instruction in instructions:
        decoded = instruction.decode()
        v = decoded.vector
        area += determinant(position, position + v)
        perimeter += decoded.steps
        position += decoded.vector
    area = abs(area) // 2
    return int(area + perimeter//2 + 1)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(INSTRUCTIONS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(INSTRUCTIONS)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
