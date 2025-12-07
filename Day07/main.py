from dataclasses import dataclass
from enum import Enum
import functools


class Cell(Enum):
    START = 'S'
    EMPTY = '.'
    SPLITTER = '^'


class Direction(Enum):
    DOWN  = (+1,  0)
    LEFT  = ( 0, -1)
    RIGHT = ( 0, +1)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def move(self, direction: Direction):
        (dx, dy) = direction.value
        return Point(self.x + dx, self.y + dy)


class Grid:

    def __init__(self, cells):
        self.cells = cells

    @property
    def rows(self):
        return len(self.cells)

    @property
    def cols(self):
        return len(self.cells[0])

    def __contains__(self, point):
        return 0 <= point.x < self.rows and 0 <= point.y < self.cols

    def __getitem__(self, point):
        return self.cells[point.x][point.y]

    @property
    def points(self):
        for x in range(self.rows):
            for y in range(self.cols):
                yield Point(x, y)

    def find(self, cell) -> Point:
        return next((point for point in self.points if self[point] == cell))


def read_input():
    with open("input.txt") as file:
        cells = [ list(map(Cell, line.rstrip('\n'))) for line in file.readlines() ]
    return Grid(cells)


def part1():
    grid = read_input()
    start = grid.find(Cell.START)

    beams = [ start ]
    seen = set(beams)
    def push(beam):
        if beam not in grid or beam in seen:
            return
        seen.add(beam)
        beams.append(beam)

    splits = 0
    while beams:
        beam = beams.pop()
        if grid[beam] == Cell.SPLITTER:
            splits += 1
            push(beam.move(Direction.LEFT))
            push(beam.move(Direction.RIGHT))
        else:
            push(beam.move(Direction.DOWN))
    print(splits)


def part2():
    grid = read_input()
    start = grid.find(Cell.START)

    @functools.lru_cache(maxsize=None)
    def timelines_from(beam):
        assert beam in grid
        if grid[beam] == Cell.SPLITTER:
            left = beam.move(Direction.LEFT)
            right = beam.move(Direction.RIGHT)
            return (timelines_from(left) if left in grid else 0) + (timelines_from(right) if right in grid else 0)
        else:
            down = beam.move(Direction.DOWN)
            return timelines_from(down) if down in grid else 1

    print(timelines_from(start))

if __name__ == "__main__":
    part1()
    part2()
