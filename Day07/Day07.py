"""AoC :: Day 7"""
from dataclasses import dataclass
import time
from typing import List
day = 7


# Parse inputs
# N.B. This changes in part two, but we change it at the class level
PIPS = {str(i): i for i in range(2, 10)} | {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

@dataclass
class Hand:
    """A hand of camel cards"""
    cards: str
    bid: int
    # cache strength
    _strength: int = None
    # class attribute
    pips = PIPS

    @property
    def strength(self):
        """The rank of the hand"""
        if self._strength is None:
            chars = set(self.cards)
            freq = {char: self.cards.count(char) for char in chars}
            vals = freq.values()
            if 5 in vals:
                self._strength = 6
            elif 4 in vals:
                self._strength = 5
            elif 3 in vals:
                if 2 in vals:
                    self._strength = 4
                else:
                    self._strength = 3
            elif 2 in vals:
                pairs = len([v for v in vals if v == 2])
                if pairs > 1:
                    self._strength = 2
                else:
                    self._strength = 1
            else:
                self._strength = 0
        # print(self._strength)
        return self._strength

    def __lt__(self, other: "Hand"):
        """Figure out which hand is best"""
        if self.strength != other.strength:
            return self.strength < other.strength
        for si, oi in zip(self.cards, other.cards):
            if self.pips[si] == self.pips[oi]:
                continue
            else:
                return self.pips[si] < self.pips[oi]
        raise ValueError(f"These two hands are identical apparently: {self}, {other}")

class Hand2(Hand):
    """Alteration of hand for part two"""
    # The values of J changes for part two
    pips = PIPS | {"J": 1}

    # As does how to calculate strength
    @property
    def strength(self):
        """the rank of the hand as in part two"""
        if self._strength is None:
            if "J" in self.cards:
                best_strength = 0
                for r in self.pips:
                    h = Hand(self.cards.replace("J", r), self.bid)
                    best_strength = max(best_strength, h.strength)
                self._strength = best_strength
            else:
                self._strength = super().strength
        return self._strength

def parse(s: str):
    """parse a hand/bid"""
    cards, bid = s.split(" ")
    return Hand(cards, int(bid))

with open('Day07/Day07.in', encoding="utf8") as f:
    HANDS = [parse(i[:-1]) for i in f.readlines()]


# part one
def part_one(hands: List[Hand]):
    """Solution to part one"""
    return sum([(r+1) * hand.bid for r, hand in enumerate(sorted(hands))])

# part two
def part_two(hands: List[Hand2]):
    """Solution to part two"""
    return sum([(r+1) * hand.bid for r, hand in enumerate(sorted(hands))])

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(HANDS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two([Hand2(h.cards, h.bid) for h in HANDS])
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
