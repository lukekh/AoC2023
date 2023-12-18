"""AoC :: Day 13"""
import time
day = 13


# parse inputs
class Pattern(list[int]):
    """
    Store a row of a pattern as an integer in binary
    e.g. ["#.##..##.", "###...##."]  -> [0b101100110, 0b111000110]
    """
    def __init__(self, __l: list[str]):
        self.length = len(__l[0])
        super().__init__([int(row.replace("#", "1").replace(".", "0"), 2) for row in __l if row])

    def horizontal_axis(self, smudges: int = 0):
        """
        Return the row idx for the horizontal axis of reflection if 
        the pattern has the right amount of smudges (or return None)
        """
        for idx in range(1, len(self)):
            ctr = 0
            for z1, z2 in zip(self[idx-1::-1], self[idx:]):
                ctr += (z1 ^ z2).bit_count()
                if ctr > smudges:
                    break
            else:
                if ctr == smudges:
                    return idx
        return None

    @staticmethod
    def compare_bints(string: str, idx: int, length: int):
        """given an index and bin integer string, split and compare"""
        L = min(idx, length - idx)
        left, right = string[idx-L:idx], string[idx+L-1:idx-1:-1]
        return int(left, 2) ^ int(right, 2)

    def vertical_axis(self, smudges: int = 0):
        """
        Return the col idx for the vertical axis of reflection if 
        the pattern has the right amount of smudges (or return None)
        """
        for idx in range(1, self.length):
            ctr = 0
            for row in self:
                b = bin(row)[2:].zfill(self.length)
                ctr += self.compare_bints(b, idx, self.length).bit_count()
                if ctr > smudges:
                    break
            else:
                if ctr == smudges:
                    return idx
        return None

    def summarize(self, smudges: int = 0):
        """
        return the cols to the left for a vertical reflection
        or the number of rows from the top * 100 for a horizontal reflection
        """
        if (v := self.vertical_axis(smudges=smudges)) is not None:
            return v
        if (v := self.horizontal_axis(smudges=smudges)) is not None:
            return v * 100
        raise ValueError("no axis of reflection found")


with open('Day13/Day13.in', encoding="utf8") as f:
    PATTERNS = [
        Pattern(p.split("\n")) for p in f.read().split("\n\n")
    ]

# part one
def part_one(patterns: list[Pattern], smudges: int = 0):
    """Solution to part one & two"""
    return sum(pattern.summarize(smudges=smudges) for pattern in patterns)

# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2023 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(PATTERNS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_one(PATTERNS, smudges=1)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
