"""AoC :: Day 15"""
from dataclasses import dataclass
import time
from typing import Dict, Literal, Optional
day = 15


# parse inputs
@dataclass
class Instruction:
    """An instruction"""
    chars: str
    operation: Literal["=", "-"]
    number: Optional[int] = None

    def __hash__(self):
        return hash(self.chars)

    def __eq__(self, other: "Instruction"):
        return self.chars == other.chars

class HASH:
    """The HASH algorithm"""
    def __init__(self):
        # dictionaries have keys ordered by insertion so are the natural
        # data structure for this challenge
        # e.g. self.boxes[box number] = {label: focal length}
        self.boxes: Dict[int, Dict[str, int]] = {n: {} for n in range(256)}

    @classmethod
    def algorithm(cls, string: str, current_value: int = 0):
        """Run the HASH algorithm on a string input"""
        for char in string:
            current_value += ord(char)
            current_value *= 17
            current_value %= 256
        return current_value

    def add(self, instruction: Instruction):
        """the result of an equals '=' operation"""
        box = self.algorithm(instruction.chars)
        self.boxes[box][instruction.chars] = instruction.number

    def rm(self, instruction: Instruction):
        """the result of a dash '-' operation"""
        box = self.algorithm(instruction.chars)
        if instruction.chars in self.boxes[box]:
            del self.boxes[box][instruction.chars]
        else:
            pass

    def do(self, instructions: list[Instruction]):
        """Run the HASH algorithm on a string input"""
        for instruction in instructions:
            match instruction.operation:
                case "=":
                    self.add(instruction)
                case "-":
                    self.rm(instruction)

    def focusing_power(self):
        """the focusing power calculation"""
        return sum(
            (b + 1) * (i+1) * length
            for b, lenses in self.boxes.items()
            for i, length in enumerate(lenses.values())
        )

def parse(s: str):
    """parse an instruction for part two"""
    if "=" in s:
        chars, number = s.split("=")
        return Instruction(chars, "=", int(number))
    if "-" in s:
        return Instruction(s[:-1], "-")
    raise ValueError(f"{s} is not a valid Instruction")

with open('Day15/Day15.in', encoding="utf8") as f:
    inputs = f.read()[:-1].split(",")
    INSTRUCTIONS = [parse(i) for i in inputs]

# part one
def part_one(args: list[str]):
    """Solution to part one"""
    return sum(HASH.algorithm(arg) for arg in args)

# part two
def part_two(instructions: list[Instruction]):
    """Solution to part two"""
    h = HASH()
    h.do(instructions)
    return h.focusing_power()

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
    a2 = part_two(INSTRUCTIONS)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
