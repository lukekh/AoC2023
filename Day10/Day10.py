"""AoC :: Day 10"""
from enum import Enum
from dataclasses import dataclass
import time
from typing import Dict, List, Literal
day = 10

# parse inputs
PIPE = Literal["|", "-", "L", "J", "7", "F"]
class Direction(Enum):
    """Directions most naturally live on the Gaussian Integers"""
    UP:    complex = -1j
    DOWN:  complex = 1j
    RIGHT: complex = 1 + 0j
    LEFT:  complex = -1 + 0j

    def __neg__(self):
        """flip a direction"""
        return Direction(-self.value)

@dataclass
class PipeMovement:
    """Encode how a pipe affects movement"""
    exit1: Direction
    exit2: Direction

    def __call__(self, item: Direction) -> Direction:
        if -item is self.exit1:
            return self.exit2
        if -item is self.exit2:
            return self.exit1
        raise KeyError(f"invalid movement {item}, can only accept {-self.exit1} or {-self.exit2} for this pipe")

    def __eq__(self, other: "PipeMovement"):
        if self.exit1 is other.exit1:
            if self.exit2 is other.exit2:
                return True
        elif self.exit1 is other.exit2:
            if self.exit2 is other.exit1:
                return True
        return False

class Pipe:
    """The representation of a pipe within the maze"""
    # How pipes correspond to exits
    EXITS: Dict[PIPE, PipeMovement] = {
        "|": PipeMovement(Direction.UP, Direction.DOWN),
        "L": PipeMovement(Direction.UP, Direction.RIGHT),
        "J": PipeMovement(Direction.UP, Direction.LEFT),
        "F": PipeMovement(Direction.DOWN, Direction.RIGHT),
        "7": PipeMovement(Direction.DOWN, Direction.LEFT),
        "-": PipeMovement(Direction.RIGHT, Direction.LEFT),
    }

    def __init__(self, kind: PIPE):
        self.kind: Pipe = kind

    @property
    def directions(self) -> PipeMovement:
        """the directions you can move out from this pipe"""
        return self.EXITS[self.kind]

    def __call__(self, direction_in: Direction) -> Direction:
        return self.EXITS[self.kind](direction_in)


@dataclass
class Position:
    """A position in the maze"""
    row: int
    col: int

    def valid(self) -> PipeMovement:
        """return the directions from this position that will lead to a pipe"""
        # MAZE.get(self(direction)) returns None if it isn't a pipe
        valid = []
        for direction in Direction:
            try:
                MAZE[self(direction)](direction)
                valid.append(direction)
            except KeyError:
                pass
        print(valid)
        return PipeMovement(exit1=valid[0], exit2=valid[1])

    def __eq__(self, other: "Position"):
        return (self.row == other.row) and (self.col == other.col)

    def __hash__(self):
        return hash((self.row, self.col, "Position"))

    def __call__(self, direction: Direction) -> "Position":
        gaussian_pos = self.col + self.row * 1j
        new_pos = gaussian_pos + direction.value
        return Position(int(new_pos.imag), int(new_pos.real))

    @property
    def pipe(self) -> "Pipe":
        """Return the pipe from the Maze at this position"""
        return MAZE[self]

MAZE: Dict[Position, Pipe] = {}

def parse(row: int, string: str):
    """insert pipes into MAZE"""
    start = None
    for col, character in enumerate(string):
        if character == "S":
            start = Position(row, col)
        elif character not in (".", "\n"):
            pos = Position(row, col)
            MAZE[pos] = Pipe(character)
    return start

with open('Day10/Day10.in', encoding="utf8") as f:
    for r, s in enumerate(f.readlines()):
        p = parse(r, s)
        if p:
            START = p

# Insert correct pipe into Maze start square
# This will help to figure out the starting direction and then
# we only need the position and direction, and we've abstracted
# the pipe away from movement
if START:
    v = START.valid()
    print(f"v = {v}")
    for char in ["|", "-", "L", "J", "7", "F"]:
        if Pipe(char).directions == v:
            print(f"starting pipe char: {char}")
            print()
            MAZE[START] = Pipe(char)
else:
    raise ValueError("There is no starting tile 'S' in the maze provided")

# part one
def part_one(start: Position):
    """
    Solution to part one
    
    return the positions the loop takes in the maze for part two
    """
    # Init counter, position and direction
    position = start
    direction = position.pipe.directions.exit1
    # store all the loop positions
    loop_positions: List[Position] = []
    # Walk around maze until we're back where we started
    while True:
        # Update position and direction
        position = position(direction)
        direction = position.pipe(direction)
        loop_positions.append(position)
        if position == start:
            break
    return len(loop_positions)//2, loop_positions

# part two
def part_two(positions: List[Position]):
    """
    Solution to part two
    
    This is maybe the most inspired solution I've ever come up with. It uses Stokes' 
    theorem (or Green's theorem or the shoelace formula, etc) to calculate the area using
    the perimeter.

    See: https://en.wikipedia.org/wiki/Shoelace_formula for more maths
    """
    def determinant(p1: Position, p2: Position):
        """return the determinant as per the shoelace formula"""
        return (p1.col * p2.row) - (p1.row * p2.col)
    # the inner sum is signed based on the direction of the loop (i.e. using the right hand rule)
    # it also calculates twice the area so divide by two
    area = abs(
        sum(determinant(pi, pj) for pi, pj in zip(positions, positions[1:] + [positions[0]]))
    ) // 2
    # subtract off the area occupied by the pipes themselves
    # this is equal to one unit of area per left/right or up/down pair
    girth = len(positions)//2 - 1
    return area - girth

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1, positions = part_one(START)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(positions)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
