"""
AoC :: Day 23

User be warned: this takes a damn long time to run
"""
from queue import PriorityQueue
from dataclasses import dataclass
import time
from typing import Literal
day = 23

@dataclass(order=True)
class Position:
    """a position in 2D space"""
    x: int
    y: int

    def __add__(self, other: "Position"):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Position"):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y, "Position"))

@dataclass(order=True)
class Path:
    """The steps and record of positions on a path"""
    steps: int
    positions: list[Position]

    @property
    def head(self):
        """The current position in this path"""
        return self.positions[-1]

    def __getitem__(self, idx: int):
        return self.positions[idx]

    def __contains__(self, val: Position):
        return val in self.positions

    def __eq__(self, other: "Path"):
        return self.positions == other.positions

    def __hash__(self):
        return hash((self.head, tuple(self.positions)))

    def step(self, p: Position, d: int):
        """step to a new position"""
        return Path(self.steps + d, self.positions + [p])

@dataclass
class Tile:
    """the kind of tile you're on"""
    position: Position
    kind: Literal["#", ".", ">", "v", "^", "<"]

    def legal(self, direction: Position, uphill: bool = False):
        """whether movement onto this tile is legal"""
        if uphill:
            return self.kind != "#"

        match self.kind:
            case "#":
                return False
            case ".":
                return True
            case ">":
                if direction.x == -1:
                    return False
                return True
            case "<":
                if direction.x == 1:
                    return False
                return True
            case "^":
                if direction.y == 1:
                    return False
                return True
            case "v":
                if direction.y == -1:
                    return False
                return True

class TrailMap:
    """A trail map"""
    def __init__(self, tiles: list[list[Tile]]):
        self.map = {tile.position: tile for row in tiles for tile in row}
        self.dims = (max(p.x for p in self.map), max(p.y for p in self.map))

    def __getitem__(self, item: Position | tuple[int, int]):
        match item:
            case Position():
                pos = item
            case tuple():
                pos = Position(**item)

        return self.map.get(pos, Tile(position=pos, kind="#"))

    def adjacent(self, position: Position, uphill: bool = False):
        """return adjacent positions"""
        directions = [
            Position( 1,  0),
            Position(-1,  0),
            Position( 0,  1),
            Position( 0, -1),
        ]
        return [
            tile.position for d in directions if (tile := self[position + d]).legal(d, uphill)
        ]

    def fork(self, position: Position):
        """return adjacent positions"""
        directions = [
            Position( 1,  0),
            Position(-1,  0),
            Position( 0,  1),
            Position( 0, -1),
        ]
        return len([
            tile.position for d in directions if (tile := self[position + d]).kind != "#"
        ]) > 2


# parse inputs
with open('Day23/Day23.in', encoding="utf8") as f:
    inputs = TrailMap([
        [
            Tile(
                Position(c, i),
                char
            ) for c, char in enumerate(row[:-1])
        ] for i, row in enumerate(f.readlines())
    ])
    START = Position(1, 0)
    END = Position(inputs.dims[0] - 1, inputs.dims[1])

# part one
def part_one(m: TrailMap, start: Position = START, end: Position = END):
    """Solution to part one"""
    forks = {pos for pos in m.map if (m[pos].kind != "#") and m.fork(pos)} | {start, end}
    print(f"len(forks): {len(forks)}")
    adjacency = {p: {} for p in forks}

    def populate_adjacency(start: Position, ends: set[Position]):
        cursors = {start}
        steps = 0
        visited = {start}
        while cursors:
            new_cursors: set[Position] = set()
            steps += 1
            for cursor in cursors:
                for adjacent in m.adjacent(cursor, uphill=True):
                    if adjacent in visited:
                        continue

                    if adjacent in ends:
                        adjacency[start][adjacent] = steps
                    else:
                        new_cursors.add(adjacent)
            visited.update(new_cursors)
            cursors = new_cursors

    for pos in forks:
        populate_adjacency(pos, forks)

    paths = PriorityQueue()
    paths.put((0, Path(0, [start])))
    max_lens: dict[Path, int] = {}

    while not paths.empty():
        _, path = paths.get()
        path: Path
        pos = path.head
        for q, d in adjacency[pos].items():
            if q not in path:
                new_path = path.step(q, d)
                if new_path.steps >= max_lens.get(new_path, 0):
                    max_lens[new_path] = new_path.steps
                    if q != end:
                        paths.put((-new_path.steps, new_path))
    return max(p.steps for p in max_lens if end in p)

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
    a1 = part_one(inputs)
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
