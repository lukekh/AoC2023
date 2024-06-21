"""AoC :: Day 22"""
from queue import PriorityQueue
from dataclasses import dataclass
import re
import time
day = 22

@dataclass(order=True)
class Brick:
    """
    A brick with a start and a stop condition
    """
    id: int
    start: tuple[int, int, int]
    stop: tuple[int, int, int]
    # Regex pattern from for inputs
    pattern = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")

    @property
    def height(self):
        """the lowest z value of a brick"""
        return self.start[2]

    @classmethod
    def parse(cls, id_: int, s: str):
        """parse a brick input"""
        groups = cls.pattern.match(s).groups()
        return Brick(
            id = id_,
            start = tuple(map(int, groups[:3])),
            stop = tuple(map(int, groups[3:]))
        )

    def range(self):
        """bricks only vary in one dimension so iterate over that dim"""
        try:
            idx = [xi != yi for xi, yi in zip(self.start, self.stop)].index(True)
        except ValueError:
            idx = 0

        v = list(self.start)

        for i in range(self.start[idx], self.stop[idx] + 1):
            v[idx] = i
            yield tuple(v)

    def __iter__(self):
        return self.range()

    def set_height(self, height: int):
        """set the bricks height"""
        delta = self.start[2] - height
        self.start = (self.start[0], self.start[1], height)
        self.stop = (self.stop[0], self.stop[1], self.stop[2] - delta)

class Tower:
    """A tower of bricks"""
    def __init__(self, bricks: list[Brick]):
        self.bricks = {brick.id: brick for brick in bricks}
        self._loc: dict[tuple[int, int, int], Brick] = {}
        self.fall()

    def fall(self):
        ordered_bricks = sorted(self.bricks.values(), key=lambda b: b.start[2])

        # init topography dict to keep track of height
        topography: dict[tuple[int, int], int] = {}
        for brick in ordered_bricks:
            height = max(topography.get((x, y), 0) for x, y, _ in brick) + 1
            brick.set_height(height)

            for x, y, z in brick:
                assert self._loc.get((x, y, z)) is None, (brick, self._loc[(x, y, z)])
                self._loc[(x, y, z)] = brick
                topography[(x, y)] = z

    def supported_by(self, brick: Brick):
        """return the bricks that support this brick"""
        support: set[int] = set()
        for x, y, z in brick:
            support.add(
                self._loc.get((x, y, z - 1), brick).id
            )
        return [self.bricks[i] for i in support - {brick.id}]

    def supporting(self, brick: Brick):
        """return the bricks that this brick is supporting"""
        support: set[int] = set()
        for x, y, z in brick:
            support.add(
                self._loc.get((x, y, z + 1), brick).id
            )
        return [self.bricks[i] for i in support - {brick.id}]

    def supporting_chain(self, brick: Brick):
        """the number of bricks that will fall if this one is disintegrated"""
        chain: set[int] = set()
        falling = PriorityQueue()
        falling.put((brick.height, brick))
        while not falling.empty():
            _, b = falling.get()
            chain.add(b.id)
            for s in self.supporting(b):
                if not {b.id for b in self.supported_by(s)} - chain:
                    falling.put((s.height, s))
        return len(chain) - 1

    def disintegrate(self, brick: Brick):
        """return whether brick can be disintegrated"""
        supporting = self.supporting(brick)
        if len(supporting) == 0:
            return True
        return all(len(self.supported_by(b)) > 1 for b in supporting)

    def part_one(self):
        """solution to part one"""
        return len([
            b for b in self.bricks.values() if self.disintegrate(b)
        ])


# parse inputs
with open('Day22/Day22.in', encoding="utf8") as f:
    inputs = Tower([Brick.parse(i, s[:-1]) for i, s in enumerate(f.readlines())])

# part one
def part_one(tower: Tower):
    """Solution to part one"""
    return tower.part_one()

# part two
def part_two(tower: Tower):
    """Solution to part two"""
    return sum(tower.supporting_chain(b) for b in tower.bricks.values())

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = inputs.part_one()
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
