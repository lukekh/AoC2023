"""AoC :: Day 2"""
from dataclasses import dataclass
import re
import time
from typing import List
day = 2

@dataclass
class Cubes:
    """Some collection of coloured cubes"""
    red: int = 0
    green: int = 0
    blue: int = 0

    def __le__(self, other: "Cubes"):
        """This makes comparison easier in part one"""
        return (self.red <= other.red) and (self.green <= other.green) and (self.blue <= other.blue)

    @property
    def power(self):
        """The equation for power described in part two"""
        return self.red * self.green * self.blue

# Parse inputs
re_game = re.compile(r"((?:\d+ \w+(?:, )?)+);?")
re_cube = re.compile(r"((\d+) (\w+))+")

def parse(s: str) -> List[Cubes]:
    """Parse a game into a list of cubes"""
    shown = re_game.findall(s)
    return [
        Cubes(**{
            color: int(n) for _, n, color in re_cube.findall(cubes)
        }) for cubes in shown
    ]

with open('Day02/Day02.in', encoding="utf8") as f:
    inputs = [parse(i) for i in f.readlines()]


# part one
def part_one(games: List[List[Cubes]], hypothesis: Cubes = Cubes(12, 13, 14)):
    """Solution to part one"""
    def possible(game: List[Cubes], hypothesis: Cubes = hypothesis):
        """Determine if a game is possible given a hypothesis game"""
        for shown in game:
            if hypothesis <= shown:
                return False
        return True

    return sum(i+1 for i, game in enumerate(games) if possible(game))

# part two
def part_two(games: List[List[Cubes]]):
    """Solution to part two"""
    min_cubes = [
        Cubes(
            red = max(cubes.red for cubes in game),
            green = max(cubes.green for cubes in game),
            blue = max(cubes.blue for cubes in game)
        ) for game in games
    ]

    return sum(cube.power for cube in min_cubes)

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
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
