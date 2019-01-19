import math
import re
from typing import NamedTuple


def extract_ints(s):
    return list(map(int, re.findall(r"-?\d+", s)))


def manhattan(p, q):
    return sum(abs(pi - qi) for pi, qi in zip(p, q))


def part_1(lines):
    nanobots = {(x, y, z): r for x, y, z, r in [extract_ints(l) for l in lines]}

    strongest = max(nanobots, key=nanobots.get)
    r = nanobots[strongest]
    return sum(1 for n in nanobots if manhattan(n, strongest) <= r)


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


class NanoBot(NamedTuple):
    pos: Point
    r: int


def get_initial_search_ranges(nanobots):
    """ Get min,max ranges for bot position coords. If all coords > 0, min will
    be 0.

    Returns:
        list of (min,max) tuples for each coord in bot position
    """
    return [(min(min(l), 0), max(l)) for l in zip(*[n.pos for n in nanobots])]


def get_initial_max_bot_count(nanobots):
    return 2 ** (math.ceil(math.log(len(nanobots), 2)))


def get_initial_box_size(xs, ys, zs):
    max_coord_range = max(r[1] - r[0] for r in (xs, ys, zs))
    return 2 ** (math.ceil(math.log(max_coord_range, 2)))


def find_bots_in_range(nanobots, xs, ys, zs, box_size):
    """
    Find the number of nanobots within each box_size section of range specified

    Yields:
        tuple(Point, number of nanobots in range, distance from origin)
    """
    r = []
    for x in range(xs[0], xs[1] + 1, box_size):
        for y in range(ys[0], ys[1] + 1, box_size):
            for z in range(zs[0], zs[1] + 1, box_size):
                count = 0
                p = Point(x, y, z)
                for bot in nanobots:
                    d = manhattan(bot.pos, p)
                    if box_size == 1:
                        d = manhattan(bot.pos, p)
                        if d <= bot.r:
                            count += 1
                    else:
                        if d // box_size - 3 <= bot.r // box_size:
                            count += 1
                yield p, count, manhattan(p, (0, 0, 0))


def sort_search_results_key(x):
    return (x[1], -x[2])


def find_min_dist_point(nanobots, xs, ys, zs, box_size, target_bot_count):
    """
    Finds closest point to the origin in range of at least `target_bot_count`
    nanobots.

    Performs a binary search by splitting the search space defined by the
    ranges `xs`, `ys` and `zs` into 'boxes' of `box_size`. The search finds the
    top-left coordinates of the box closest to the origin that encompasses the
    ranges of at least `target_bot_count` nanobots. Repeatedly halving the
    search space and `box_size` until performing a point-by-point grid search
    (`box_size==1`) where the single best point is found and the search
    terminates.
    """
    in_range = [
        x
        for x in find_bots_in_range(nanobots, xs, ys, zs, box_size)
        if x[1] >= target_bot_count
    ]

    while in_range:
        in_range.sort(key=sort_search_results_key)
        best = in_range[-1]

        if box_size == 1:
            return best
        else:
            next_box_size = box_size // 2
            xs = (best[0].x, best[0].x + next_box_size)
            ys = (best[0].y, best[0].y + next_box_size)
            zs = (best[0].z, best[0].z + next_box_size)
            next_result = find_min_dist_point(
                nanobots, xs, ys, zs, next_box_size, target_bot_count
            )

            if next_result is None:
                in_range.pop()
            else:
                return next_result
    return None


def part_2(lines):
    """
    Uses a 'double' binary search to find the closest point to the origin with
    the maximum number of nanobots in range.

    The first binary search is `find_min_dist_point` function above.

    The `while` loop within this function performs a binary search on a minimum
    target number of nanobots in range of a point, starting from 1. It uses the
    first binary search repeatedly to find the closest point to the origin with
    the current target number of nanobots in range.

    If a point is found with the current target, the target is increased by the
    current maximum bot count to try and find a better result. Else, the
    current maximum is halved and the target is decreased by this amount.
    """
    nanobots = [
        NanoBot(Point(x, y, z), r) for x, y, z, r in [extract_ints(l) for l in lines]
    ]

    xs, ys, zs = get_initial_search_ranges(nanobots)
    box_size = get_initial_box_size(xs, ys, zs)
    max_bot_count = get_initial_max_bot_count(nanobots)
    best = None
    target_bot_count = 1
    searched = {}

    while True:
        if target_bot_count not in searched:
            searched[target_bot_count] = find_min_dist_point(
                nanobots, xs, ys, zs, box_size, target_bot_count
            )
        r = searched[target_bot_count]

        if r is None:
            if max_bot_count > 1:
                max_bot_count = max_bot_count // 2
            # try to find point with half as many nanobots in range
            target_bot_count = max(1, target_bot_count - max_bot_count)
        else:
            if best is None or r[1] > best[1]:
                best = r
            if max_bot_count == 1:
                break
            # try to find point with half as many more nanobots in range
            target_bot_count += max_bot_count
    return best


def main(puzzle_input_f):
    lines = [l for l in puzzle_input_f.read().splitlines() if l]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2(lines))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
