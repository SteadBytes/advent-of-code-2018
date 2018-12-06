from collections import defaultdict

# SICP inspired me to get 'streamy' with this one


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def coords_limits(coords):
    min_x = min(coords, key=lambda c: c[0])[0]
    max_x = max(coords, key=lambda c: c[0])[0]
    min_y = min(coords, key=lambda c: c[1])[1]
    max_y = max(coords, key=lambda c: c[1])[1]

    return ((min_x, max_x), (min_y, max_y))


def gen_locations(x_lims, y_lims):
    for x in range(x_lims[0], x_lims[1] + 1):
        for y in range(y_lims[0], y_lims[1] + 1):
            yield (x, y)


def gen_locations_coords(coords):
    x_lims, y_lims = coords_limits(coords)
    for x, y in gen_locations(x_lims, y_lims):
        for cx, cy in coords:
            yield ((x, y), (cx, cy))


def gen_locations_coords_dists(coords):
    for (x, y), (cx, cy) in gen_locations_coords(coords):
        d = manhattan_distance(cx, cy, x, y)
        yield ((x, y), (cx, cy), d)


def part_1(coords):
    closest_coord_map = {}
    closest_coord_dists = defaultdict(lambda: float("inf"))
    for (x, y), (cx, cy), d in gen_locations_coords_dists(coords):
        closest = closest_coord_dists[(x, y)]
        if d < closest:
            closest_coord_map[(x, y)] = (cx, cy)
            closest_coord_dists[(x, y)] = d
        elif d == closest and closest_coord_map[(x, y)] != (cx, cy):
            closest_coord_map[(x, y)] = None

    x_lims, y_lims = coords_limits(coords)
    coords_areas = defaultdict(int)
    for xy, coord in closest_coord_map.items():
        if coord is None:
            continue
        if xy[0] in x_lims or xy[1] in y_lims:
            coords_areas[coord] = float("-inf")
        coords_areas[coord] += 1
    return max(coords_areas.values())


def part_2(coords):
    total_dists_to_coords = defaultdict(int)
    for (x, y), (cx, cy), d in gen_locations_coords_dists(coords):
        total_dists_to_coords[(x, y)] += d
    return len([l for l, d in total_dists_to_coords.items() if d < 10000])


def main(puzzle_input_f):
    lines = puzzle_input_f.read().split("\n")
    coords = [
        tuple([int(s.strip()) for s in line.split(",")]) for line in lines if line
    ]

    print("Part 1: ", part_1(coords))
    print("Part 2: ", part_2(coords))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
