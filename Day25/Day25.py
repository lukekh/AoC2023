"""AoC :: Day 25"""
from random import choice
import time
day = 25


class Components(dict[str, set]):
    """Representation of components as a double-dict"""

    def copy(self):
        return Components({k: v.copy() for k, v in self.items()})

    def connections(self, component: str):
        """Enquire about a component and its connections"""
        return self.get(component, set())

    def connect(self, c1: str, c2: str):
        """Connect two components"""
        if c1 != c2:
            self[c1] = self.get(c1, set()) | {c2}
            self[c2] = self.get(c2, set()) | {c1}

    def disconnect(self, c1: str, c2: str):
        """Disconnect two components"""
        if c1 != c2:
            self[c1] = self.get(c1, set()) - {c2}
            self[c2] = self.get(c2, set()) - {c1}

    def groups(self):
        """Find all connected components har har har"""
        groups: list[set] = []
        for component in self:
            for group in groups:
                if component in group:
                    break
            else:
                new_group = {component} | self[component]
                new_members = new_group

                while new_members:
                    n = set()
                    for member in new_members:
                        n |= self[member]
                    new_members = n - new_group
                    new_group |= n

                groups.append(new_group)

        return groups

    def contract(self, c1: str, c2: str):
        """contract graph by absorbing c2 into c1"""
        if c2 not in self[c1]:
            raise KeyError(f"the component {c2} is not connected to {c1}")
        for c in self[c2].copy():
            self.connect(c1, c)
            self.disconnect(c2, c)
        del self[c2]


# parse inputs
with open('Day25/Day25.in', encoding="utf8") as f:
    COMPONENTS = Components()

    for row in f.readlines():
        name, connections = row.split(": ")
        for connection in connections.split(" "):
            COMPONENTS.connect(name, connection.strip())


# part one
def part_one(components: Components):
    """
    Solution to part one

    Uses Karger's Algorithm tracking the number of nodes absorbed via the contractions
    """
    while True:
        g = components.copy()
        k: dict[str, dict[str, int]] = {c: {d: 1 for d in components[c]} for c in components}
        ctr: dict[str, int] = {c: 1 for c in components}

        while len(g) > 2:
            c = choice(list(g))
            d = choice(list(g[c]))
            g.contract(c, d)
            ctr[c] = ctr[c] + ctr[d]
            del ctr[d]
            k[c] = {x: k[c].get(x, 0) + k[d].get(x, 0) for x in k[c] | k[d] if x not in (c, d)}
            for y in k[c]:
                k[y][c] = k[c][y]
                if d in k[y]:
                    del k[y][d]
            del k[d]

        k1, k2 = list(k)
        if k[k1][k2] == 3:
            return ctr[k1] * ctr[k2]

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(COMPONENTS)
    t1 += time.time()
    print(f"Answer: {a1}")

    print(f":: total runtime: {t1: .4f}s ::")


if __name__ == "__main__":
    main()
