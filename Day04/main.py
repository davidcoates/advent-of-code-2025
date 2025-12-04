from dataclasses import dataclass


PAPER = '@'
BLANK = '.'

@dataclass
class Grid:
    cells: list[list[str]]

    @property
    def rows(self):
        return len(self.cells)

    @property
    def cols(self):
        return len(self.cells[0])

    def in_bounds(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols

    def surrounding(self, i, j):
        directions = [ (dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0 ]
        return [ self.cells[i + dx][j + dy] for (dx, dy) in directions if self.in_bounds(i + dx, j + dy) ]


def read_input():
    with open("input.txt") as file:
        return Grid([ list(line.rstrip('\n')) for line in file.readlines() ])

def is_removable_roll(grid, i, j):
    return grid.cells[i][j] == PAPER and len([cell for cell in grid.surrounding(i, j) if cell == PAPER]) < 4

def part1():
    grid = read_input()
    count = 0
    for i in range(grid.rows):
        for j in range(grid.cols):
            if is_removable_roll(grid, i, j):
                count += 1
    print(count)

def part2():
    grid = read_input()
    count = 0
    while True:
        done = True
        for i in range(grid.rows):
            for j in range(grid.cols):
                if is_removable_roll(grid, i, j):
                    grid.cells[i][j] = BLANK
                    count += 1
                    done = False
        if done:
            break
    print(count)

if __name__ == "__main__":
    part1()
    part2()
