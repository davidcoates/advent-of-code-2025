from dataclasses import dataclass
from enum import Enum, auto


class Direction(Enum):
    L = auto()
    R = auto()


@dataclass
class Rotation:
    direction: Direction
    distance: int

    @staticmethod
    def from_string(x):
        return Rotation(Direction[x[0]], int(x[1:]))


def read_input():
    with open("input.txt") as file:
        return [ Rotation.from_string(line.rstrip('\n')) for line in file.readlines() ]


@dataclass
class Dial:
    position: int = 50

    TOTAL_POSITIONS = 100

    def flip(self) -> 'Dial':
        return Dial((Dial.TOTAL_POSITIONS - self.position) % Dial.TOTAL_POSITIONS)

    def rotate(self, rotation: Rotation) -> 'Dial':
        match rotation.direction:
            case Direction.R:
                return Dial((self.position + rotation.distance) % Dial.TOTAL_POSITIONS)
            case Direction.L:
                return self.flip().rotate(Rotation(Direction.R, rotation.distance)).flip()

    def count_clicks_to_zero(self, rotation: Rotation) -> int:
        match rotation.direction:
            case Direction.R:
                return (self.position + rotation.distance) // Dial.TOTAL_POSITIONS
            case Direction.L:
                return self.flip().count_clicks_to_zero(Rotation(Direction.R, rotation.distance))


def part1():
    dial = Dial()
    password = 0
    for rotation in read_input():
        dial = dial.rotate(rotation)
        if dial.position == 0:
            password += 1
    print(password)


def part2():
    dial = Dial()
    password = 0
    for rotation in read_input():
        password += dial.count_clicks_to_zero(rotation)
        dial = dial.rotate(rotation)
    print(password)


if __name__ == "__main__":
    part1()
    part2()
