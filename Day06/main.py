from dataclasses import dataclass
from enum import StrEnum
import math


class Operation(StrEnum):
    ADDITION = '+'
    MULTIPLICATION = '*'


@dataclass
class Problem:
    args: list[int]
    op: Operation

    def eval(self):
        match self.op:
            case Operation.ADDITION:
                return sum(self.args)
            case Operation.MULTIPLICATION:
                return math.prod(self.args)


def transpose(grid):
    cols = []
    for col in range(len(grid[0])):
        cols.append(''.join(grid[row][col] for row in range(len(grid))))
    return cols


def split_rows(grid, sep):
    rows = [[]]
    for row in grid:
        if all(chr == sep for chr in row):
            rows.append([])
        else:
            rows[-1].append(row)
    return rows


def split_columns(grid, sep):
    return [ transpose(rows) for rows in split_rows(transpose(grid), sep) ]


def read_input(columnar: bool = False):
    with open("input.txt") as file:
        lines = [ line.rstrip('\n') for line in file.readlines() ]
    cols = split_columns(lines, sep=' ')
    problems = []
    for col in cols:
        op = Operation(col[-1][0])
        args = col[:-1]
        if columnar:
            args = transpose(args)
        args = list(map(int, args))
        problems.append(Problem(args, op))
    return problems


def part1():
    problems = read_input()
    print(sum(problem.eval() for problem in problems))


def part2():
    problems = read_input(columnar=True)
    print(sum(problem.eval() for problem in problems))


if __name__ == "__main__":
    part1()
    part2()
