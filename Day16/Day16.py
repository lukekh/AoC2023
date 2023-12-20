"""AoC :: Day 16"""
from enum import Enum
import time
from typing import Dict, Set, Tuple
day = 16


# parse inputs
class Direction(Enum):
    """the different directions of travel"""
    UP    = 1j
    LEFT  = -1+0j
    DOWN  = -1j
    RIGHT = 1+0j

    def __radd__(self, other: complex):
        return other + self.value

class Mirror(Enum):
    """the different mirror types"""
    FORWARD_SLASH = "/"
    BACK_SLASH    = "\\"

    def move(self, position: complex, direction: Direction):
        """the resulting movements of a beam"""
        match self:
            case Mirror.FORWARD_SLASH:
                match direction:
                    case Direction.UP:
                        return [(position + Direction.RIGHT, Direction.RIGHT)]
                    case Direction.LEFT:
                        return [(position + Direction.DOWN, Direction.DOWN)]
                    case Direction.DOWN:
                        return [(position + Direction.LEFT, Direction.LEFT)]
                    case Direction.RIGHT:
                        return [(position + Direction.UP, Direction.UP)]
            case Mirror.BACK_SLASH:
                match direction:
                    case Direction.UP:
                        return [(position + Direction.LEFT, Direction.LEFT)]
                    case Direction.LEFT:
                        return [(position + Direction.UP, Direction.UP)]
                    case Direction.DOWN:
                        return [(position + Direction.RIGHT, Direction.RIGHT)]
                    case Direction.RIGHT:
                        return [(position + Direction.DOWN, Direction.DOWN)]

class Splitter(Enum):
    """the different splitter types"""
    VERTICAL      = "|"
    HORIZONTAL    = "-"

    def move(self, position: complex, direction: Direction):
        """the resulting movements of a beam"""
        match self:
            case Splitter.VERTICAL:
                if direction in (Direction.UP, Direction.DOWN):
                    return [(position + direction, direction)]
                return [(position + Direction.UP, Direction.UP), (position + Direction.DOWN, Direction.DOWN)]
            case Splitter.HORIZONTAL:
                if direction in (Direction.LEFT, Direction.RIGHT):
                    return [(position + direction, direction)]
                return [(position + Direction.LEFT, Direction.LEFT), (position + Direction.RIGHT, Direction.RIGHT)]


class Contraption:
    """a contraption with mirrors and splitters"""
    def __init__(self, width: int = None, height: int = None):
        self.width = width
        self.height = height
        self.grid: Dict[complex, Mirror | Splitter] = {}

    def move(self, position: complex, direction: Direction):
        """determine the next step of a beam"""
        if position in self.grid:
            obj = self.grid[position]
            return obj.move(position, direction)
        return [(position + direction.value, direction)]

    def valid(self, position: complex):
        """test that a beam is in bounds"""
        return (0 <= position.real < self.width) and (0 <= position.imag < self.height)

    def __call__(self, beam: Tuple[complex, Direction] = (0+0j, Direction.LEFT)):
        beams: Set[Tuple[complex, Direction]] = {beam}
        curr_beams = [beam]
        while curr_beams:
            new_beams = []
            for position, direction in curr_beams:
                for n in self.move(position, direction):
                    if self.valid(n[0]) and (n not in beams):
                        beams.add(n)
                        new_beams.append(n)
            curr_beams = new_beams
        return len({pos for pos, _ in beams})

with open('Day16/Day16.in', encoding="utf8") as f:
    inputs = [i[:-1] for i in f.readlines()]
    WIDTH = len(inputs[0])
    HEIGHT = len(inputs)
    CONTRAPTION = Contraption(width=WIDTH, height=HEIGHT)
    for row, string in enumerate(inputs):
        for col, char in enumerate(string):
            pos = complex(col, HEIGHT - row - 1)
            if char in ("/", "\\"):
                CONTRAPTION.grid[pos] = Mirror(char)
            elif char in ("|", "-"):
                CONTRAPTION.grid[pos] = Splitter(char)

    INIT_BEAM = (complex(0, HEIGHT - 1), Direction.RIGHT)


# part one
def part_one(beam: Tuple[complex, Direction], contraption: Contraption = CONTRAPTION):
    """Solution to part one"""
    return contraption(beam)

# part two
def part_two(contraption: Contraption = CONTRAPTION):
    """Solution to part two"""
    right = complex(contraption.width - 1, 0)
    top = complex(0, contraption.height - 1)
    beams = (
        [(h*1j, Direction.RIGHT) for h in range(contraption.height)] +
        [(right + h*1j, Direction.LEFT) for h in range(contraption.height)] +
        [(w + 0j, Direction.UP) for w in range(contraption.width)] +
        [(w + top, Direction.DOWN) for w in range(contraption.width)]
    )
    return max(contraption(beam) for beam in beams)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(INIT_BEAM)
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
