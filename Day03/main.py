
def read_input():
    with open("input.txt") as file:
        return [ [ int(chr) for chr in line.rstrip('\n') ] for line in file.readlines() ]

def concat(x: int, y: int) -> int:
    return int(f"{x}{y}")

def max_joltage(bank: list[int], n: int) -> int:
    if n == 1:
        return max(bank)
    else:
        i = max(range(len(bank) - (n - 1)), key=lambda i: bank[i])
        return concat(bank[i], max_joltage(bank[i+1:], n - 1))

def part1():
    print(sum(max_joltage(bank, 2) for bank in read_input()))

def part2():
    print(sum(max_joltage(bank, 12) for bank in read_input()))

if __name__ == "__main__":
    part1()
    part2()
