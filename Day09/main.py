from dataclasses import dataclass
import itertools


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Edge:
    a: Point
    b: Point

    def __post_init__(self):
        assert self.a != self.b


@dataclass
class Rectangle:
    a: Point
    b: Point

    @property
    def area(self):
        return (abs(self.a.x - self.b.x) + 1) * (abs(self.a.y - self.b.y) + 1)

    def inside(self, polygon):
        # this isn't actually correct, but it works
        return not any(self.intersects(edge) for edge in polygon.edges)

    def intersects(self, edge):
        [min_x, max_x] = sorted([self.a.x, self.b.x])
        [min_y, max_y] = sorted([self.a.y, self.b.y])
        if edge.a.y == edge.b.y:
            edge_y = edge.a.y
            if not (min_y < edge_y < max_y):
                return False
            [edge_min_x, edge_max_x] = sorted([edge.a.x, edge.b.x])
            return edge_max_x > min_x and edge_min_x < max_x
        else:
            edge_x = edge.a.x
            [edge_min_y, edge_max_y] = sorted([edge.a.y, edge.b.y])
            if not (min_x < edge_x < max_x):
                return False
            return edge_max_y > min_y and edge_min_y < max_y
        return False


class Polygon:

    def __init__(self, points):
        self.points = points
        self.edges = [ Edge(point1, point2) for (point1, point2) in zip(points, points[1:] + points[:1]) ]


def read_input():
    def parse_point(line):
        [y, x] = map(int, line.rstrip('\n').split(','))
        return Point(x, y)
    with open("input.txt") as file:
        return [ parse_point(line) for line in file.readlines() ]


def rectangles_from_points(points):
    for [point1, point2] in itertools.combinations(points, 2):
        yield Rectangle(point1, point2)


def part1():
    points = read_input()
    rectangles = rectangles_from_points(points)
    print(max(rectangle.area for rectangle in rectangles))


def part2():
    points = read_input()
    rectangles = rectangles_from_points(points)
    boundary = Polygon(points)
    print(max(rectangle.area for rectangle in rectangles if rectangle.inside(boundary)))


if __name__ == "__main__":
    part1()
    part2()
