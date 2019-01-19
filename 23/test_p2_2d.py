import pytest
from p2_2d import *


def test_find_nanobots_in_range():
    nanobots = [
        Bot(Point(8, 8), 4),
        Bot(Point(24, 36), 4),
        Bot(Point(32, 28), 4),
        Bot(Point(28, 12), 8),
    ]
    xs, ys = get_initial_search_ranges(nanobots)
    box_size = get_initial_box_size(xs, ys)
    r = find_nanobots_in_range(nanobots, xs, ys, box_size)
    assert list(r) == [(Point(0, 0), 4, 0)]

    box_size = box_size // 2
    xs, ys = [(c, c + box_size) for c in (0, 0)]
    r = find_nanobots_in_range(nanobots, xs, ys, box_size)
    assert list(r) == [
        (Point(0, 0), 4, 0),
        (Point(0, 32), 4, 32),
        (Point(32, 0), 4, 32),
        (Point(32, 32), 4, 64),
    ]


@pytest.mark.parametrize(
    "xs,ys,expected",
    [
        ((0, 2), (0, 2), 2),
        ((0, 4), (0, 2), 4),
        ((0, 4), (0, 4), 4),
        ((0, 16), (0, 2), 16),
        ((0, 16), (0, 16), 16),
        ((0, 18), (0, 16), 32),
        ((0, 16), (0, 18), 32),
        ((10, 12), (10, 12), 2),
        ((10, 16), (10, 12), 8),
        ((10, 18), (10, 12), 8),
        ((0, 2), (0, -2), 2),
        ((0, 2), (-2, 2), 4),
        ((0, 2), (-3, 2), 8),
        ((-2, 2), (0, 2), 4),
    ],
)
def test_get_initial_box_size(xs, ys, expected):
    assert get_initial_box_size(xs, ys) == expected


@pytest.mark.parametrize(
    "bot_positions,expected",
    [
        ([(0, 0), (0, 0), (0, 0)], [(0, 0), (0, 0)]),
        ([(0, 1), (0, 0), (0, 0)], [(0, 0), (0, 1)]),
        ([(0, 1), (1, 0), (0, 0)], [(0, 1), (0, 1)]),
        ([(0, 1), (1, 0), (1, 1)], [(0, 1), (0, 1)]),
        ([(10, 1), (1, 0), (1, 1)], [(0, 10), (0, 1)]),
        ([(0, 0), (0, 10), (5, 0)], [(0, 5), (0, 10)]),
        ([(10, 1), (1, 10), (1, 1)], [(0, 10), (0, 10)]),
        ([(10, 1), (1, 10), (20, 1)], [(0, 20), (0, 10)]),
        ([(10, -1), (1, 10), (1, 1)], [(0, 10), (-1, 10)]),
        ([(10, -1), (-1, 10), (1, 1)], [(-1, 10), (-1, 10)]),
    ],
)
def test_get_initial_search_ranges(bot_positions, expected):
    nanobots = [Bot(Point(x, y), 1) for x, y in bot_positions]
    assert get_initial_search_ranges(nanobots) == expected


@pytest.mark.parametrize(
    "search_results,expected",
    [
        ([(Point(x=0, y=0), 4, 0)], [(Point(x=0, y=0), 4, 0)]),
        (
            [(Point(x=0, y=0), 4, 0), (Point(x=1, y=0), 5, 1)],
            [(Point(x=0, y=0), 4, 0), (Point(x=1, y=0), 5, 1)],
        ),
        (
            [(Point(x=0, y=0), 4, 0), (Point(x=1, y=0), 4, 1)],
            [(Point(x=1, y=0), 4, 1), (Point(x=0, y=0), 4, 0)],
        ),
        (
            [
                (Point(x=0, y=0), 4, 0),
                (Point(x=10, y=5), 10, 15),
                (Point(x=1, y=0), 4, 1),
            ],
            [
                (Point(x=1, y=0), 4, 1),
                (Point(x=0, y=0), 4, 0),
                (Point(x=10, y=5), 10, 15),
            ],
        ),
        (
            [
                (Point(x=0, y=0), 4, 0),
                (Point(x=-20, y=5), 10, 25),
                (Point(x=10, y=5), 10, 15),
                (Point(x=1, y=0), 4, 1),
            ],
            [
                (Point(x=1, y=0), 4, 1),
                (Point(x=0, y=0), 4, 0),
                (Point(x=-20, y=5), 10, 25),
                (Point(x=10, y=5), 10, 15),
            ],
        ),
    ],
)
def test_sort_search_results_key(search_results, expected):
    assert sorted(search_results, key=sort_search_results_key) == expected


@pytest.mark.parametrize(
    "nanobots,possible_points,expected_count,expected_dist",
    [
        ([(8, 8, 4), (24, 36, 4), (32, 28, 4), (28, 12, 8)], [(4, 8), (8, 4)], 1, 12),
        ([(8, 8, 4), (24, 36, 4), (32, 28, 4), (28, 12, 200)], [(4, 8), (7, 5)], 2, 12),
        (
            [
                (10, 12, 2),
                (12, 14, 2),
                (16, 12, 4),
                (14, 14, 6),
                (50, 50, 200),
                (10, 10, 5),
            ],
            [(12, 12)],
            6,
            24,
        ),
    ],
)
def test_brute_force(nanobots, possible_points, expected_count, expected_dist):
    # multiple possible points with same count and distance from (0, 0)
    p, c, d = brute_force([Bot(Point(b[0], b[1]), b[2]) for b in nanobots])
    assert p in possible_points and (c, d) == (expected_count, expected_dist)


@pytest.mark.parametrize(
    "nanobots,possible_points,expected_count,expected_dist",
    [
        ([(8, 8, 4), (24, 36, 4), (32, 28, 4), (28, 12, 8)], [(4, 8), (8, 4)], 1, 12),
        ([(8, 8, 4), (24, 36, 4), (32, 28, 4), (28, 12, 200)], [(4, 8), (7, 5)], 2, 12),
        (
            [
                (10, 12, 2),
                (12, 14, 2),
                (16, 12, 4),
                (14, 14, 6),
                (50, 50, 200),
                (10, 10, 5),
            ],
            [(12, 12)],
            6,
            24,
        ),
    ],
)
def test_solve(nanobots, possible_points, expected_count, expected_dist):
    p, c, d = solve([Bot(Point(b[0], b[1]), b[2]) for b in nanobots])
    assert p in possible_points and (c, d) == (expected_count, expected_dist)
