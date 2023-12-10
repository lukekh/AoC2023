"""AoC :: Day 10"""
from dataclasses import dataclass
import time
from typing import Dict, List, Literal, Set
day = 10

# parse inputs
PIPES = Literal["|", "-", "L", "J", "7", "F"]
OTHER = Literal[".", "S"]
DIRECTION = Literal["UP", "DOWN", "LEFT", "RIGHT"]

def flip(direction: DIRECTION) -> DIRECTION:
    """flip a direction"""
    match direction:
        case "UP":
            return "DOWN"
        case "DOWN":
            return "UP"
        case "LEFT":
            return "RIGHT"
        case "RIGHT":
            return "LEFT"

@dataclass
class Position:
    """A position in the maze"""
    row: int
    col: int

    def valid(self) -> Set[DIRECTION]:
        """return the valid pipes nearby that can be entered from this position"""
        valid = set()
        if MAZE.get(self("UP")) and MAZE.get(self("UP")).kind in ("|", "7", "F"):
            valid.add("UP")
        if MAZE.get(self("DOWN")) and MAZE.get(self("DOWN")).kind in ("|", "J", "L"):
            valid.add("DOWN")
        if MAZE.get(self("RIGHT")) and MAZE.get(self("RIGHT")).kind in ("-", "J", "7"):
            valid.add("RIGHT")
        if MAZE.get(self("LEFT")) and MAZE.get(self("LEFT")).kind in ("-", "F", "L"):
            valid.add("LEFT")
        return valid

    def __eq__(self, other: "Position"):
        return (self.row == other.row) and (self.col == other.col)

    def __hash__(self):
        return hash((self.row, self.col, "Position"))

    def __call__(self, direction: DIRECTION):
        match direction:
            case "UP":
                return Position(self.row - 1, self.col)
            case "DOWN":
                return Position(self.row + 1, self.col)
            case "LEFT":
                return Position(self.row, self.col - 1)
            case "RIGHT":
                return Position(self.row, self.col + 1)

@dataclass
class Pipe:
    """The representation of a pipe within the maze"""
    kind: PIPES
    position: Position

    @property
    def directions(self) -> Set[DIRECTION]:
        """the directions you can move out from this pipe"""
        match self.kind:
            case "|":
                return {"UP", "DOWN"}
            case "-":
                return {"LEFT", "RIGHT"}
            case "L":
                return {"UP", "RIGHT"}
            case "J":
                return {"UP", "LEFT"}
            case "7":
                return {"DOWN", "LEFT"}
            case "F":
                return {"DOWN", "RIGHT"}

    def __call__(self, in_: DIRECTION) -> DIRECTION:
        directions = self.directions
        if (flipped := flip(in_)) in directions:
            out = (directions ^ {flipped}).pop()
            return out
        raise ValueError(f"you cannot travel {in_} into the {self.kind} pipe")


MAZE: Dict[Position, Pipe] = {}

def parse(row: int, string: str):
    """insert pipes into MAZE"""
    start = None
    for col, char in enumerate(string):
        if char == "S":
            start = Position(row, col)
        elif char not in (".", "\n"):
            pos = Position(row, col)
            MAZE[pos] = Pipe(char, pos)
    return start

with open('Day10/Day10.in', encoding="utf8") as f:
    for r, s in enumerate(f.readlines()):
        p = parse(r, s)
        if p:
            START = p

if START:
    v = START.valid()
    for kind in ["|", "-", "L", "J", "7", "F"]:
        if Pipe(kind, START).directions == v:
            MAZE[START] = Pipe(kind, START)

# part one
def part_one(start: Position):
    """
    Solution to part one
    
    return the positions the loop takes in the maze for part two
    """
    d = start.valid().pop()
    loop_positions: List[DIRECTION] = [start(d)]
    # step into maze
    ahead = MAZE[start(d)]
    i = 1
    while ahead.position != start:
        d = ahead(d)
        loop_positions.append(ahead.position(d))
        ahead = MAZE[ahead.position(d)]
        i += 1
    return i//2, loop_positions

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
    # the inner sum returns a signed area based on the direction of the loop (i.e. using the right hand rule)
    # it also calculates twice the area 
    area = abs(
        sum(determinant(pi, pj) for pi, pj in zip(positions, positions[1:] + [positions[0]]))
    ) // 2
    # subtract off the area occupied by the pipes themselves
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
