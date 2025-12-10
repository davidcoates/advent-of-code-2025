from collections import defaultdict
from dataclasses import dataclass
import heapq
import z3


@dataclass
class Machine:
    indicator_lights: int
    buttons: list[list[int]]
    joltages: list[int]


def read_input():
    def interior(word):
        return word[1:-1]
    def parse_tuple(word):
        return tuple(map(int, interior(word).split(',')))
    def parse_indicator_lights(word):
        bits = 0
        for chr in reversed(interior(word)):
            bits *= 2
            if chr == '#':
                bits += 1
        return bits
    def parse_machine(line):
        words =line.rstrip('\n').split(' ')
        indicator_lights = parse_indicator_lights(words[0])
        buttons = [ parse_tuple(word) for word in words[1:-1] ]
        joltages = parse_tuple(words[-1])
        return Machine(indicator_lights, buttons, joltages)
    with open("input.txt") as file:
        return [ parse_machine(line) for line in file.readlines() ]


def min_button_presses_for_indicators(machine: Machine):
    n = len(machine.joltages)
    start_node = 0
    distances = {}
    priority_queue = [(0, start_node)]
    while priority_queue:
        distance, node = heapq.heappop(priority_queue)
        if node == machine.indicator_lights:
            return distance
        if node in distances:
            continue
        distances[node] = distance
        for button in machine.buttons:
            next_node = node
            for bit in button:
                next_node ^= (1 << bit)
            if next_node not in distances:
                heapq.heappush(priority_queue, (distance + 1, next_node))
    assert False


def min_button_presses_for_joltages(machine: Machine):
    button_press_counts = [ z3.Int(f"b{i}") for i, button in enumerate(machine.buttons) ]
    solver = z3.Optimize()
    for button_press_count in button_press_counts:
        solver.add(button_press_count >= 0)
    for bit, bit_count in enumerate(machine.joltages):
        solver.add(bit_count == z3.Sum(
            [ button_press_count for button_press_count, button in zip(button_press_counts, machine.buttons) if bit in button ]
        ))
    solver.minimize(z3.Sum(button_press_counts))
    solver.check()
    model = solver.model()
    return sum(model[button_press_count].as_long() for button_press_count in button_press_counts)


def part1():
    machines = read_input()
    print(sum(min_button_presses_for_indicators(machine) for machine in machines))


def part2():
    machines = read_input()
    print(sum(min_button_presses_for_joltages(machine) for machine in machines))


if __name__ == "__main__":
    part1()
    part2()
