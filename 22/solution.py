import heapq
from collections import deque, namedtuple


class Point(namedtuple("Point", ["x", "y"])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    @property
    def adjacent(self):
        return [self.up, self.down, self.left, self.right]

    @property
    def left(self):
        return self + Point(-1, 0)

    @property
    def right(self):
        return self + Point(1, 0)

    @property
    def up(self):
        return self + Point(0, -1)

    @property
    def down(self):
        return self + Point(0, 1)


MOUTH = Point(0, 0)
(ROCKY, WET, NARROW) = (NEITHER, TORCH, CLIMBING) = 0, 1, 2


def cave_regions(depth, target: Point, limit: Point = None):
    if limit is None:
        limit = target

    erosion_levels = {}
    region_types = {}

    for y in range(limit.y + 1):
        for x in range(limit.x + 1):
            pt = Point(x, y)
            if pt == MOUTH or pt == target:
                geo_i = 0
            elif y == 0:
                geo_i = x * 16807
            elif x == 0:
                geo_i = y * 48271
            else:
                geo_i = erosion_levels[pt.left] * erosion_levels[pt.up]
            erosion_level = (geo_i + depth) % 20183
            erosion_levels[pt] = erosion_level
            region_types[pt] = erosion_level % 3
    return region_types


def show_cave(regions, target, limit=None):
    x_max = limit.x if limit else max(p.x for p in regions)
    y_max = limit.y if limit else max(p.y for p in regions)

    for y in range(y_max + 1):
        l = []
        for x in range(x_max + 1):
            p = Point(x, y)
            if p == MOUTH:
                l.append("M")
            elif p == target:
                l.append("T")
            else:
                l.append({ROCKY: ".", WET: "=", NARROW: "|"}[regions[p]])
        print("".join(l))


def part_1(depth, target: Point):
    return sum(cave_regions(depth, target).values())


def part_2(depth, target):
    # can go outside of square needed for p1
    limit = Point(target.x + 1000, target.y + 1000)
    regions = cave_regions(depth, target, limit)

    def is_valid(region, equipment):
        if region == ROCKY and (equipment == CLIMBING or equipment == TORCH):
            return True
        if region == WET and (equipment == CLIMBING or equipment == NEITHER):
            return True
        if region == NARROW and (equipment == TORCH or equipment == NEITHER):
            return True
        return False

    # time, point, equipment
    heap = [(0, MOUTH, TORCH)]
    seen = set()

    while heap:
        time, point, equipment = heapq.heappop(heap)
        if (point, equipment) == (target, TORCH):
            return time
        if (point, equipment) in seen:
            continue
        seen.add((point, equipment))

        for eq in range(3):
            if is_valid(regions[point], eq):
                heapq.heappush(heap, (time + 7, point, eq))

        for p in point.adjacent:
            if p.x < 0 or p.y < 0:
                continue
            if is_valid(regions[p], equipment):
                heapq.heappush(heap, (time + 1, p, equipment))


def main(puzzle_input_f):
    lines = puzzle_input_f.read().splitlines()
    d, t = [l.split(": ")[1] for l in lines if l]
    depth = int(d)
    x, y = [int(x) for x in t.split(",")]

    target = Point(x, y)
    print("Depth: ", depth)
    print("Target:", target)

    print("Part 1: ", part_1(depth, target))
    print("Part 2: ", part_2(depth, target))


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
