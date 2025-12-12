from dataclasses import dataclass


@dataclass
class Shape:
    id: int
    cells: list[list[bool]]

    def __post_init__(self):
        self._size = sum(1 for row in self.cells for cell in row if cell)

    @property
    def size(self):
        return self._size


@dataclass
class Region:
    width: int
    length: int
    shape_freqs: list[int]

    @property
    def size(self):
        return self.width * self.length


def lines_to_blocks(lines):
    blocks = [[]]
    for line in lines:
        if line:
            blocks[-1].append(line)
        else:
            blocks.append([])
    return blocks


def read_input():

    with open("input.txt") as file:
        blocks = lines_to_blocks(line.rstrip('\n') for line in file.readlines())

    def parse_shape(block):
        id = int(block[0][:-1])
        cells = [ [ (True if chr == '#' else False) for chr in row ] for row in block[1:] ]
        return Shape(id, cells)
    shapes = [ parse_shape(block) for block in blocks[:-1] ]

    def parse_region(line):
        [size_str, shape_freqs_str] = line.split(': ')
        [width, length] = map(int, size_str.split('x'))
        shape_freqs = list(map(int, shape_freqs_str.split(' ')))
        return Region(width, length, shape_freqs)
    regions = [ parse_region(line) for line in blocks[-1] ]

    return shapes, regions


def region_fits_shapes(region, shapes):
    num_blocks = (region.width // 3) * (region.length // 3)
    if sum(region.shape_freqs) <= num_blocks:
        return True
    num_cells = sum(shapes[shape_id].size * freq for shape_id, freq in enumerate(region.shape_freqs))
    if num_cells > region.size:
        return False
    assert False


def part1():
    shapes, regions = read_input()
    print(sum(1 for region in regions if region_fits_shapes(region, shapes)))


if __name__ == "__main__":
    part1()
