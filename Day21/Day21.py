"""AoC :: Day 21"""
import time
day = 21


# parse inputs
with open('Day21/Day21.in', encoding="utf8") as f:
    inputs = f.read()
    GARDEN = [[char != "#" for char in row] for row in inputs.split("\n") if row]
    s_idx = inputs.index("S")
    START = (
        s_idx // (len(GARDEN[0]) + 1),
        s_idx % (len(GARDEN[0]) + 1)
    )
    MAX = (len(GARDEN), len(GARDEN[0]))

# part one
def adjacent(pos, garden: list[list[bool]], boundary = MAX):
    """return adjacent points"""
    pts = [
        (pos[0] + 1, pos[1]),
        (pos[0] - 1, pos[1]),
        (pos[0], pos[1] + 1),
        (pos[0], pos[1] - 1),
    ]
    return [p for p in pts if (0 <= p[0] < boundary[0]) and (0 <= p[1] < boundary[1]) and garden[p[0]][p[1]]]

def bfs(garden: list[list[bool]], start: tuple[int, int] = START):
    """Use breadth first search to find distance from starting position of each tile"""
    positions = {start}
    visited: set[tuple[int, int]] = set()
    bfs_map: dict[tuple[int, int], int] = {}

    # init
    steps = 0
    while positions:
        new_positions = set()
        for position in positions:
            visited.add(position)
            bfs_map[position] = steps
            new_positions.update(adjacent(position, garden))
        visited.update(positions)
        steps += 1
        new_positions -= visited

        positions = new_positions

    return bfs_map


def part_one(garden: list[list[bool]], start: tuple[int, int] = START, steps = 64):
    """Solution to part one"""
    bfs_map = bfs(garden=garden, start=start)
    b = steps % 2

    n = len([
        pt for pt, d in bfs_map.items() if (d <= steps) and ((d % 2) == b)
    ])

    # We can use the breadth first search in part two
    return n, bfs_map

def centred_square_decomposition(i: int, parity: bool = True):
    """
    return the odd and even parity components of the centred square number
    
    note: returns odd part, then even part
    """
    if (i + parity) % 2:
        return (i + 1)**2, i**2
    else:
        return i**2, (i + 1)**2

# part two
def part_two(bfs_map: dict[tuple[int, int], int], steps = 26_501_365, dims = MAX):
    """
    Solution to part two

    This partially relies on the fact that the garden is a square and an odd stride and would need to
    be corrected if that changed.
    """
    # n is the number of tiles away from the centre tile we can get if we travel in a straight line
    n = steps // dims[0]
    r = steps % dims[0]
    parity = steps % 2
    odd, even = centred_square_decomposition(n, parity)
    full_tiles = (
        odd * len([pt for pt, d in bfs_map.items() if (d % 2) == parity]) +
        even * len([pt for pt, d in bfs_map.items() if not (d % 2) == parity])
    )

    odd_corners, even_corners = (n, -(n + 1)) if (n % 2) == parity else (-(n + 1), n)
    corners = (
        odd_corners * len([pt for pt, d in bfs_map.items() if (d % 2) == parity and (d > r)]) + 
        even_corners * len([pt for pt, d in bfs_map.items() if not (d % 2) == parity and (d > r)])
    )

    return full_tiles + corners

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1, bfs_map = part_one(GARDEN)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(bfs_map)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
