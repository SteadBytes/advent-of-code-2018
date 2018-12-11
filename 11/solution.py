from collections import defaultdict

GRID_LIMIT = 300


def cell_power(x, y, serial_number):
    rack_id = x + 10
    p = ((rack_id * y) + serial_number) * rack_id
    hundreds = (p // 100) % 10
    return hundreds - 5


def build_partial_sums(serial_number):
    partial_sums = defaultdict(int)

    def ps(x, y):
        return (
            cell_power(x, y, serial_number)
            + partial_sums[x, y - 1]
            + partial_sums[x - 1, y]
            - partial_sums[x - 1, y - 1]
        )

    for y in range(GRID_LIMIT):
        for x in range(GRID_LIMIT):
            partial_sums[x, y] = ps(x, y)
    return partial_sums


def find_max_square(partial_sums, size_min=3, size_max=4):
    grid_sums = {}
    for s in range(size_min, size_max):
        for y in range(s - 1, GRID_LIMIT):
            for x in range(s - 1, GRID_LIMIT):
                grid_sums[x - s + 1, y - s + 1, s] = (
                    partial_sums[x, y]
                    + partial_sums[x - s, y - s]
                    - partial_sums[x - s, y]
                    - partial_sums[x, y - s]
                )

    max_pos = max(grid_sums, key=grid_sums.get)
    max_sum = grid_sums[max_pos]
    return max_pos[0], max_pos[1], max_pos[2]


def part_1(partial_sums):
    return find_max_square(partial_sums)[:2]


def part_2(partial_sums):
    return find_max_square(partial_sums, 2, 301)


def main(puzzle_input_f):
    serial_number = int(f.read())
    partial_sums = build_partial_sums(serial_number)

    print("Part 1: ", part_1(partial_sums))
    print("Part 2: ", part_2(partial_sums))


if __name__ == "__main__":
    with open("input.txt") as f:

        main(f)
