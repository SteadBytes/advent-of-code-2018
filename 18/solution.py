from collections import namedtuple


class Point(namedtuple("Point", ["x", "y"])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def adjacent(self):
        vels = [
            Point(*v)
            for v in [
                (-1, -1),
                (0, -1),
                (1, -1),
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0),
            ]
        ]
        return [self + v for v in vels]


def point_in_bounds(p: Point, size):
    return 0 <= p.x < size and 0 <= p.y < size


def parse_input(lines):
    # example input is smaller than the 50*50 stated in puzzle
    size = len(lines)

    trees = set()
    lumberyard = set()

    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            p = Point(x, y)
            if ch == "|":
                trees.add(p)
            elif ch == "#":
                lumberyard.add(p)

    return trees, lumberyard, size


def gen_acres(trees, lumberyard, size):
    while True:
        next_trees = set()
        next_lumberyard = set()

        for y in range(size):
            for x in range(size):
                p = Point(x, y)
                adj = [p2 for p2 in p.adjacent() if point_in_bounds(p2, size)]
                adj_lumberyard = len([p2 for p2 in adj if p2 in lumberyard])
                adj_tree = len([p2 for p2 in adj if p2 in trees])
                if p in trees:
                    if adj_lumberyard >= 3:
                        next_lumberyard.add(p)
                    else:
                        next_trees.add(p)
                elif p in lumberyard:
                    if adj_lumberyard > 0 and adj_tree > 0:
                        next_lumberyard.add(p)
                else:
                    if adj_tree >= 3:
                        next_trees.add(p)
        trees = next_trees
        lumberyard = next_lumberyard
        yield frozenset(trees), frozenset(lumberyard)


def part_1(input_lines):
    trees, lumberyard, size = parse_input(input_lines)
    g = gen_acres(trees, lumberyard, size)
    for _ in range(10):
        trees, lumberyard = next(g)
    return len(trees) * len(lumberyard)


def part_2(input_lines):
    trees, lumberyard, size = parse_input(input_lines)
    g = gen_acres(trees, lumberyard, size)

    # grid eventually enters repeating cycle
    # find interval of repeat
    seen = set()
    repeat_i = None
    for i, next_acres in enumerate(g):
        if next_acres in seen:
            if repeat_i is None:
                repeat_i = i
            else:
                break
            seen = set()
        seen.add(next_acres)

    repeat_interval = i - repeat_i
    # generator currently at first state of the repeating cycle
    # now can 'repeat' process for part 1
    for _ in range(100000000 % repeat_interval):
        trees, lumberyard = next(g)
    return len(trees) * len(lumberyard)


def main(puzzle_input_f):
    lines = puzzle_input_f.read().splitlines()

    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2(lines))


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
