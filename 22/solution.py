from collections import namedtuple


class Point(namedtuple("Point", ["y", "x"])):
    """ Order of y,x swapped from usual x,y to enable sorting in reading order
    by default. AoC grid systems often have x increasing right y increasing down
    """

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)


def part_1(depth, target: Point):
    mouth = Point(0, 0)

    erosion_levels = {}
    region_types = {}

    for y in range(target.y + 1):
        for x in range(target.x + 1):
            pt = Point(y, x)
            if pt == mouth or pt == target:
                geo_i = 0
            elif y == 0:
                geo_i = x * 16807
            elif x == 0:
                geo_i = y * 48271
            else:
                geo_i = (
                    erosion_levels[pt + Point(-1, 0)]
                    * erosion_levels[pt + Point(0, -1)]
                )
            erosion_level = (geo_i + depth) % 20183
            erosion_levels[pt] = erosion_level
            region_types[pt] = erosion_level % 3

    return sum(region_types.values())


def part_2():
    pass


def main(puzzle_input_f):
    lines = puzzle_input_f.read().splitlines()
    d, t = [l.split(": ")[1] for l in lines if l]
    depth = int(d)
    x, y = [int(x) for x in t.split(",")]

    target = Point(y, x)

    print("Part 1: ", part_1(depth, target))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
