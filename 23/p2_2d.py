import math
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Bot(NamedTuple):
    pos: Point
    r: int


def manhattan(p, q):
    return sum(abs(pi - qi) for pi, qi in zip(p, q))


def get_initial_search_ranges(nanobots):
    """ Get min,max ranges for bot position coords. If all coords > 0, min will
    be 0.

    Returns:
        list of (min,max) tuples for each coord in bot position
    """
    return [(min(min(l), 0), max(l)) for l in zip(*[n.pos for n in nanobots])]


def get_initial_max_bot_count(nanobots):
    return 2 ** (math.ceil(math.log(len(nanobots), 2)))


def get_initial_box_size(xs, ys):
    max_coord_range = max(r[1] - r[0] for r in (xs, ys))
    return 2 ** (math.ceil(math.log(max_coord_range, 2)))


def find_nanobots_in_range(nanobots, xs, ys, box_size):
    """
    Find the number of nanobots within each box_size section of range specified
    """
    r = []
    for x in range(xs[0], xs[1] + 1, box_size):
        for y in range(ys[0], ys[1] + 1, box_size):
            count = 0
            p = Point(x, y)
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


def find_min_dist_point(nanobots, xs, ys, box_size, target_bot_count):
    """
    Find the closest point to the origin with target_bot_count nanobots in range
    """
    in_range = [
        x
        for x in find_nanobots_in_range(nanobots, xs, ys, box_size)
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
            next_result = find_min_dist_point(
                nanobots, xs, ys, next_box_size, target_bot_count
            )

            if next_result is None:
                in_range.pop()
            else:
                return next_result
    return None


def solve(nanobots):
    xs, ys = get_initial_search_ranges(nanobots)

    box_size = get_initial_box_size(xs, ys)

    max_bot_count = get_initial_max_bot_count(nanobots)
    best = None
    target_bot_count = 1
    searched = {}
    while True:
        if target_bot_count not in searched:
            searched[target_bot_count] = find_min_dist_point(
                nanobots, xs, ys, box_size, target_bot_count
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


def brute_force(nanobots):
    xs, ys = get_initial_search_ranges(nanobots)

    best_point = Point(xs[1], xs[1])
    best_count = 0
    for x in range(xs[0], xs[1] + 1):
        for y in range(ys[0], ys[1] + 1):
            p = Point(x, y)
            count = 0
            for bot in (b for b in nanobots if b.pos != p):
                if manhattan(bot.pos, p) <= bot.r:
                    count += 1
            if count > best_count:
                best_count = count
                best_point = p
            elif count == best_count:
                if manhattan(p, (0, 0)) < manhattan(best_point, (0, 0)):
                    best_point = p
    return best_point, best_count, manhattan(best_point, (0, 0))
