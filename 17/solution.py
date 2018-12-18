import re
from collections import defaultdict, namedtuple


class Point(namedtuple("Point", ["x", "y"])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


spring = Point(500, 0)


def part_1():
    pass


def part_2():
    pass


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

    y_min = min(clay, key=lambda p: p.y).y
    y_max = max(clay, key=lambda p: p.y).y

    # TODO: Recursive 'fill' algorithm - track settled and flowing water? set()?

    print("Part 1: ", part_1())
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "example_input.txt")) as f:
        main(f)
