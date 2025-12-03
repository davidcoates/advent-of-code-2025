import functools


def read_input():
    with open("input.txt") as file:
        return [ [ int(chr) for chr in line.rstrip('\n') ] for line in file.readlines() ]

def concat(*xs: int) -> int:
    return int(''.join(str(x) for x in xs))

def max_joltage(bank: list[int], m: int) -> int:

    @functools.lru_cache(maxsize=None)
    def max_joltage_(i: int, m: int):
        if m == 1:
            return max(bank[i:])
        elif m == len(bank) - i:
            return concat(*bank[i:])
        else:
            return max(concat(bank[i], max_joltage_(i+1, m-1)), max_joltage_(i+1, m))

    return max_joltage_(0, m)


def part1():
    print(sum(max_joltage(bank, 2) for bank in read_input()))

def part2():
    print(sum(max_joltage(bank, 12) for bank in read_input()))

if __name__ == "__main__":
    part1()
    part2()
