from dataclasses import dataclass
import functools


@dataclass
class Devices:
    neighbours: dict[str, list[str]]

    def num_paths_from(self, device: str, must_include = {}):
        @functools.lru_cache(maxsize=None)
        def num_paths_from_impl(device: str, must_include: frozenset):
            if device == "out":
                return 0 if must_include else 1
            if device in must_include:
                must_include = must_include.difference({device})
            return sum(num_paths_from_impl(neighbour, must_include) for neighbour in self.neighbours[device])
        return num_paths_from_impl(device, frozenset(must_include))


def read_input():
    def parse_line(line):
        [device, outputs] = line.rstrip('\n').split(': ')
        return device, outputs.split(' ')
    with open("input.txt") as file:
        return Devices(dict(parse_line(line) for line in file.readlines()))


def part1():
    devices = read_input()
    print(devices.num_paths_from("you"))


def part2():
    devices = read_input()
    print(devices.num_paths_from("svr", must_include={'dac', 'fft'}))


if __name__ == "__main__":
    part1()
    part2()
