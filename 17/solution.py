import re
from collections import defaultdict, namedtuple
from enum import Enum
import sys
sys.setrecursionlimit(10000)


class Point(namedtuple("Point", ["x", "y"])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Direction(Enum):
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)


spring = Point(500, 0)


class Simulation:
    def __init__(self, clay):
        self.clay = clay
        self.settled = set()
        self.flowing = set()
        self.y_min = min(clay, key=lambda p: p.y).y
        self.y_max = max(clay, key=lambda p: p.y).y

    def run(self):
        self.flow(spring, Direction.DOWN)

    def flow(self, p: Point, d: Direction):
        self.flowing.add(p)
        beneath = p + Direction.DOWN.value

        if not self.clay[beneath]:
            if beneath not in self.flowing and 1 <= beneath.y <= self.y_max:
                self.flow(beneath, Direction.DOWN)
            if beneath not in self.settled:
                return False

        left = p + Direction.LEFT.value
        right = p + Direction.RIGHT.value

        l_flowing = left in self.flowing
        r_flowing = right in self.flowing

        l_filled = self.clay[left] or not l_flowing and self.flow(left, Direction.LEFT)
        r_filled = self.clay[right] or not r_flowing and self.flow(right, Direction.RIGHT)

        if d == Direction.DOWN and l_filled and r_filled:
            self.settled.add(p)
            while left in self.flowing:
                self.settled.add(left)
                left += Direction.LEFT.value

            while right in self.flowing:
                self.settled.add(right)
                right += Direction.RIGHT.value

        if d == Direction.LEFT and (self.clay[left] or l_filled):
            return True
        elif d == Direction.RIGHT and (self.clay[right] or r_filled):
            return True
        return False

    def in_bounds(self, p: Point):
        return self.y_min <= p.y <= self.y_max


def part_1(completed_sim):
    water = (p for p in completed_sim.flowing | completed_sim.settled)
    return len([p for p in water if completed_sim.in_bounds(p)])


def part_2(completed_sim):
    return len([p for p in completed_sim.settled if completed_sim.in_bounds(p)])


def main(puzzle_input_f):
    clay = defaultdict(bool)

    for l in puzzle_input_f.read().splitlines():
        vein_start, vein_range = [
            [int(x) for x in re.findall(r"\d+", s)] for s in l.split(", ")
        ]
        vein_start = vein_start[0]
        ax = l[0]
        vein_range[1] += 1
        if ax == "x":
            for y in range(*vein_range):
                clay[Point(vein_start, y)] = True
        else:
            for x in range(*vein_range):
                clay[Point(x, vein_start)] = True
    sim = Simulation(clay)
    sim.run()
    print("Part 1: ", part_1(sim))
    print("Part 2: ", part_2(sim))


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
