from dataclasses import dataclass
import itertools
import math


@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int

    def distance_squared(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2


class Network:

    def __init__(self, boxes: list[Point3D]):
        self._circuits_by_box = { box : frozenset({box}) for box in boxes }
        distances = { (box1, box2) : box1.distance_squared(box2) for [box1, box2] in itertools.combinations(boxes, 2) }
        self._pending_connections = sorted(distances.keys(), key=lambda key: distances[key], reverse=True)

    @property
    def circuits(self):
        return frozenset(self._circuits_by_box.values())

    def connect_boxes(self) -> tuple[Point3D, Point3D] | None:
        assert self._pending_connections
        (box1, box2) = self._pending_connections.pop()
        if self._circuits_by_box[box1] == self._circuits_by_box[box2]:
            return None
        new_circuit = self._circuits_by_box[box1] | self._circuits_by_box[box2]
        for box in new_circuit:
            self._circuits_by_box[box] = new_circuit
        return (box1, box2)


def read_input():
    def parse_line(line):
        [x, y, z] = list(map(int, line.rstrip('\n').split(',')))
        return Point3D(x, y, z)
    with open("input.txt") as file:
        boxes = [ parse_line(line) for line in file.readlines() ]
    return Network(boxes)


def part1():
    network = read_input()
    num_connections = 1000
    for _ in range(num_connections):
        network.connect_boxes()
    largest_circuits = sorted(map(len, network.circuits), reverse=True)[:3]
    print(math.prod(largest_circuits))


def part2():
    network = read_input()
    last_connection = None
    while len(network.circuits) > 1:
        connection = network.connect_boxes()
        if connection is not None:
            last_connection = connection
    assert last_connection is not None
    (box1, box2) = last_connection
    print(box1.x * box2.x)


if __name__ == "__main__":
    part1()
    part2()
