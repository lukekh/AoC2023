"""AoC :: Day 8"""
import math
import re
import time
from typing import Dict, List, Literal
day = 8


# Parse inputs
class Node:
    """
    A node within the network
    
    N.B Node holds a global map of the network as new nodes are added
    """
    # Global network
    network: Dict[str, "Node"] = {}

    def __init__(self, name: str, left: str, right: str):
        self.name = name
        self._left = left
        self._right = right
        # Add Node to global network
        self.network[name] = self
        # To aide with part two
        self.ghost_terminus = self.name[2] == "Z"

    @property
    def left(self):
        """return the left node"""
        return self.network[self._left]

    @property
    def right(self):
        """return the left node"""
        return self.network[self._right]

    def __str__(self):
        return f"Node[{self.name} = ({self._left}, {self._right})]"

    def __repr__(self):
        return str(self)

    def __call__(self, direction: Literal["L", "R"]):
        match direction:
            case "L":
                return self.left
            case "R":
                return self.right
            case _:
                raise ValueError(f"direction must be 'L' or 'R', got {direction}")


re_node = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
with open('Day08/Day08.in', encoding="utf8") as f:
    INSTRUCTIONS, map_string = f.read().split("\n\n")
    INIT_NODE = None
    TERMINAL_NODE = None
    for row in map_string[:-1].split("\n"):
        n = Node(*re_node.match(row).groups())
        if n.name == "AAA":
            INIT_NODE = n
        if n.name == "ZZZ":
            TERMINAL_NODE = n

if INIT_NODE is None:
    raise ValueError("Initial node AAA is missing from inputs")
if TERMINAL_NODE is None:
    raise ValueError("Terminal node ZZZ is missing from inputs")


# part one
def part_one(instructions: str, node: Node, terminus: Node):
    """Solution to part one"""
    i = 0
    N = len(instructions)
    while node != terminus:
        instruction = instructions[i % N]
        node = node(instruction)
        i += 1
    return i

# part two
def part_two(instructions: str, nodes: List[Node]):
    """
    Solution to part two
    
    This works because it seems that each Node ghost-terminates in perfect cycles,
    which is not necessarily guaranteed. Thus, it checks this condition is met and
    raises a ValueError if it fails on your particular instructions.
    """
    N = len(instructions)
    ghost_terminals = []
    for node in nodes:
        j = 0
        t = -1
        terminated = False
        while True:
            instruction = instructions[j % N]
            node = node(instruction)
            j += 1
            if node.ghost_terminus:
                if not terminated:
                    t = j
                    terminated = True
                else:
                    if t != j - t:
                        raise ValueError("Using math.lcm won't work with these inputs, good luck")
                    ghost_terminals.append(t)
                    break
    return math.lcm(*ghost_terminals)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(INSTRUCTIONS, INIT_NODE, TERMINAL_NODE)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(INSTRUCTIONS, [node for name, node in Node.network.items() if name[2] == "A"])
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
