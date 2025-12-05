from dataclasses import dataclass


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __post_init__(self):
        assert self.start <= self.end

    def __contains__(self, x: int):
        return self.start <= x <= self.end

    def __len__(self):
        return self.end - self.start + 1

    def _union(self, other):
        return Range(min(self.start, other.start), max(self.end, other.end))

    def intersects(self, other) -> bool:
        return len(self._union(other)) < len(self) + len(other)

    def union(self, other):
        assert self.intersects(other)
        return self._union(other)


class Ranges:

    def __init__(self):
        self._disjoint_ranges = set()

    def add(self, new_range):
        for range in self._disjoint_ranges:
            if new_range.intersects(range):
                self._disjoint_ranges.remove(range)
                self.add(range.union(new_range))
                return
        self._disjoint_ranges.add(new_range)

    def __contains__(self, id):
        return any(id in range for range in self._disjoint_ranges)

    def __len__(self):
        return sum(len(range) for range in self._disjoint_ranges)


def read_input():
    with open("input.txt") as file:
        def read_block():
            while True:
                line = file.readline().rstrip('\n')
                if line:
                    yield line
                else:
                    break
        ranges = Ranges()
        for line in read_block():
            [ start, end ] = [ int(word) for word in line.split('-') ]
            ranges.add(Range(start, end))
        ids = []
        for line in read_block():
            ids.append(int(line))
    return ranges, ids

def part1():
    ranges, ids = read_input()
    fresh_ids = [id for id in ids if id in ranges]
    print(len(fresh_ids))

def part2():
    ranges, _ = read_input()
    print(len(ranges))

if __name__ == "__main__":
    part1()
    part2()
