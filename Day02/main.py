from dataclasses import dataclass

@dataclass
class Range:
    first: int
    last: int

    def __post_init__(self):
        assert self.first <= self.last

    def __iter__(self):
        return iter(range(self.first, self.last + 1))


def read_input():
    def parse_range(x):
        first, last = x.split('-')
        return Range(int(first), int(last))
    with open("input.txt") as file:
        return [ parse_range(range) for range in file.readlines()[0].rstrip('\n').split(',') ]


def is_repeated(x: str, m: int) -> bool:
    """
    is the string x comprised of m idential sequences of digits?
    """
    assert m >= 2
    n = len(x)
    if n % m != 0:
        return False
    l = n // m
    return x == x[:l] * m


def part1():
    ranges = read_input()
    def is_invalid(id):
        return is_repeated(str(id), 2)
    print(sum(id for range_ in ranges for id in range_ if is_invalid(id)))


def part2():
    ranges = read_input()
    def is_invalid(id):
        x = str(id)
        return any(is_repeated(x, m) for m in range(2, len(x)+1))
    print(sum(id for range_ in ranges for id in range_ if is_invalid(id)))


if __name__ == "__main__":
    part1()
    part2()
