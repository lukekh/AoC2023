"""AoC :: Day 17"""
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
import time
from typing import Dict
day = 17


class Direction(Enum):
    """the different directions of travel"""
    UP    = 1j
    LEFT  = -1+0j
    DOWN  = -1j
    RIGHT = 1+0j

    def __radd__(self, other: complex):
        return other + self.value


@dataclass(order=True)
class Cursor:
    """a cursor moving along the grid"""
    loss: int
    # State
    position: complex = field(compare=False)
    direction: Direction = field(compare=False)
    # counts the number of times this direction has been travelled in
    ctr: int = field(compare=False)

    def valid(self, minimum: int = None, maximum: int = None) -> tuple[Direction, ...]:
        """return valid next directions given a direction"""
        if minimum and (self.ctr < minimum - 1):
            return (self.direction,)
        match self.direction:
            case Direction.UP:
                if self.ctr >= maximum - 1:
                    return (Direction.LEFT, Direction.RIGHT)
                return (Direction.LEFT, Direction.UP, Direction.RIGHT)
            case Direction.LEFT:
                if self.ctr >= maximum - 1:
                    return (Direction.DOWN, Direction.UP)
                return (Direction.DOWN, Direction.LEFT, Direction.UP)
            case Direction.DOWN:
                if self.ctr >= maximum - 1:
                    return (Direction.RIGHT, Direction.LEFT)
                return (Direction.RIGHT, Direction.DOWN, Direction.LEFT)
            case Direction.RIGHT:
                if self.ctr >= maximum - 1:
                    return (Direction.UP, Direction.DOWN)
                return (Direction.UP, Direction.RIGHT, Direction.DOWN)

    def __hash__(self):
        return hash((self.position, self.direction, self.loss))

class Grid:
    """a grid of values that determines heat loss"""
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.grid: Dict[complex, int] = {}

    def __getitem__(self, item: complex):
        return self.grid[item]

    def valid(self, position: complex):
        """check that a cursor is in a valid spot"""
        return (0 <= position.real < self.width) and (0 <= position.imag < self.height)

    def A_star(self, init: complex, terminus: complex, minimum: int = None, maximum: int = 3):
        """do A* on the grid"""
        history: dict[tuple[complex, Direction], int] = {}
        cursors = PriorityQueue()

        for direction in Direction:
            if self.valid(init + direction):
                position = init + direction
                history[(position, direction, 0)] = self[position]
                cursors.put(Cursor(self[position], position, direction, 0))
        while True:
            cursor = cursors.get_nowait()
            cursor: Cursor
            for direction in cursor.valid(minimum, maximum):
                new_position = cursor.position + direction
                if new_position == terminus:
                    return cursor.loss + self.grid[terminus]
                if self.valid(new_position):
                    new_ctr = (cursor.ctr + 1) if direction is cursor.direction else 0
                    new_loss = cursor.loss + self.grid[new_position]
                    if (new_position, direction, new_ctr) in history:
                        if new_loss < history[(new_position, direction, new_ctr)]:
                            history[(new_position, direction, new_ctr)] = new_loss
                        else:
                            continue
                    else:
                        history[(new_position, direction, new_ctr)] = new_loss
                    cursors.put(
                        Cursor(new_loss, new_position, direction, new_ctr)
                    )

# parse inputs
with open('Day17/Day17.in', encoding="utf8") as f:
    inputs = [i[:-1] for i in f.readlines()]
    HEIGHT = len(inputs)
    WIDTH = len(inputs[0])
    MAP = Grid(HEIGHT, WIDTH)
    for row, string in enumerate(inputs):
        for col, char in enumerate(string):
            pos = complex(col, HEIGHT - row - 1)
            MAP.grid[pos] = int(char)
    INIT = complex(0, HEIGHT-1)
    TERMINUS = complex(WIDTH-1, 0)


# part one
def part_one(init: complex, terminus: complex, grid: Grid = MAP):
    """Solution to part one"""
    return grid.A_star(init, terminus)

# part two
def part_two(init: complex, terminus: complex, grid: Grid = MAP):
    """Solution to part two"""
    return grid.A_star(init, terminus, 4, 10)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(INIT, TERMINUS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(INIT, TERMINUS)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
