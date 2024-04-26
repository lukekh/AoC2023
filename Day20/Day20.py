"""AoC :: Day 20"""
from collections import deque
from dataclasses import dataclass, field
import math
import re
import time
from typing import Any, Literal, Optional
day = 20

@dataclass
class Pulse:
    """A pulse queue item"""
    strength: bool
    from_: str
    affects: list[str]

PULSES: deque[Pulse] = deque()

# Create an rx Exception to exit part 2
class rxException(Exception):
    """Bail out of part 2 once you get this exception"""

@dataclass
class AbstractModule:
    """
    Base class for modules
    
    Note:
    * `%` is a flip-flop module
    * `&` is a conjunction module
    """
    id: str
    kind: Optional[Literal["%", "&", "broadcaster"]] = None
    parents: Optional[list[str]] = field(default_factory=list)
    children: Optional[list[str]] = field(default_factory=list)
    state: bool = False
    memory: dict[str, bool] = field(default_factory=dict)

    def __call__(self, pulse: Pulse):
        match self.kind:
            case "%":
                if pulse.strength:
                    return None

                self.state = not self.state

                return Pulse(
                    strength = self.state,
                    from_ = self.id,
                    affects = self.children
                )
            case "&":
                self.memory[pulse.from_] = pulse.strength

                return Pulse(
                    strength = not all(self.memory.values()) if pulse.strength else True,
                    from_ = self.id,
                    affects = self.children
                )
            case "broadcaster":
                return Pulse(
                    strength = pulse.strength,
                    from_ = self.id,
                    affects = self.children
                )
            case _:
                # Some modules have no kind and I guess are considered dead
                # Relevant in part 2 surprise surprise
                if (not pulse.strength) and self.id == "rx":
                    raise StopIteration()

    def has_parent(self, parent: str):
        """Add a parent to this module"""
        self.parents.append(parent)

    def __add__(self, other: "AbstractModule"):
        return AbstractModule(
            kind = self.kind if self.kind is not None else other.kind,
            id = self.id,
            parents = self.parents + other.parents,
            children = self.children + other.children,
            state = self.state,
            memory = self.memory | other.memory
        )


class Modules:
    """A collection of modules"""
    def __init__(self):
        self._modules: dict[str, AbstractModule] = {}
        self.pulses: deque[Pulse] = deque()
        # Counters
        self.lows = 0
        self.highs = 0

    @property
    def broadcaster(self):
        """returns the unique broadcaster module"""
        return self["broadcaster"]

    def __getitem__(self, item: str):
        if item not in self._modules:
            new_module = AbstractModule(id = item)
            self._modules[item] = new_module
        return self._modules[item]

    def __setitem__(self, item: str, val: AbstractModule):
        self._modules[item] = val

    def initialise(self):
        """Initialise the memory of the conjunction modules"""
        for m in self._modules.values():
            match m.kind:
                case "&":
                    m.memory = {parent: False for parent in m.parents}
                case _:
                    pass

    def add(self, module: AbstractModule):
        """add a new module unknown to self or update with more information"""
        self[module.id] += module
        for child in module.children:
            self[child].has_parent(module.id)

    def resolve(self):
        """resolve the pulse that has been in the queue for longest"""
        pulse = self.pulses.popleft()
        # update counter
        match pulse.strength:
            case True:
                self.highs += len(pulse.affects)
            case False:
                self.lows += len(pulse.affects)

        # calculate effects
        for recipient in pulse.affects:
            if (response := self[recipient](pulse)) is not None:
                self.pulses.append(response)

    def button(self):
        """push the button"""
        self.pulses.append(Pulse(
            strength=False,
            from_="button",
            affects=["broadcaster"]
        ))
        

MODULES = Modules()

re_row = re.compile(r"([%&]|broadcaster)(\w+)? -> (.+)")
def parse(s: str, modules: Modules):
    """Parse a row from inputs"""
    match_ = re_row.match(s)
    kind = match_.group(1)
    if kind in ("%", "&"):
        id_ = match_.group(2)
        affects = [child.strip() for child in match_.group(3).split(",")]
        modules.add(AbstractModule(
            kind = kind,
            id = id_,
            children = affects
        ))
    elif kind == "broadcaster":
        affects = [child.strip() for child in match_.group(3).split(",")]
        modules.add(AbstractModule(
            kind = kind,
            id = kind,
            children = affects
        ))


with open('Day20/Day20.in', encoding="utf8") as f:
    for line in f.readlines():
        parse(line, MODULES)

MODULES.initialise()

# part one
def part_one(modules: Modules, n: int = 1000):
    """Solution to part one"""
    for _ in range(n):
        modules.button()
        while True:
            try:
                modules.resolve()
            except IndexError:
                break
    return modules.lows * modules.highs

# part two
make_bin = lambda l: bin(sum(2**i for i, j in enumerate(l) if j))[2:].zfill(8)
def part_two(modules: Modules):
    """Solution to part two"""
    press_ctr = 0
    ids = {"xz", "jn", "rb", "hh", "rq", "bg", "ts", "jl"}
    mem = {id_: None for id_ in ids}
    last = {id_: 0 for id_ in ids}
    cycle = {id_: 0 for id_ in ids}
    while ids:
        try:
            modules.resolve()
        except IndexError:
            press_ctr += 1
            modules.button()
            for id_ in ids.copy():
                if mem[id_] != modules[id_].state:
                    if cycle[id_] == press_ctr - last[id_]:
                        ids.remove(id_)
                        print(cycle)
                    else:
                        cycle[id_] = press_ctr - last[id_]
                        last[id_] = press_ctr
                mem[id_] = modules[id_].state
    print(cycle)

    return press_ctr

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(MODULES)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = 2 # part_two(MODULES)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
