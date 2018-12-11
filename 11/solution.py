from copy import deepcopy
from collections import defaultdict


def cell_power(x, y, serial_number):
    rack_id = x + 10
    p = ((rack_id * y) + serial_number) * rack_id
    hundreds = (p // 100) % 10
    return hundreds - 5


def part_1(serial_number):
    partial_sums = defaultdict(int)

    def ps(x, y):
        return (
            cell_power(x, y, serial_number)
            + partial_sums[x, y - 1]
            + partial_sums[x - 1, y]
            - partial_sums[x - 1, y - 1]
        )

    for y in range(300):
        for x in range(300):
            partial_sums[x, y] = ps(x, y)

    width = height = 3
    grid_sums = {}
    for y in range(300):
        for x in range(300):
            grid_sums[x, y] = (
                partial_sums[x, y]
                + partial_sums[x - width, y - height]
                - partial_sums[x - width, y]
                - partial_sums[x, y - height]
            )

    max_pos = max(grid_sums, key=grid_sums.get)
    max_sum = grid_sums[max_pos]
    return max_pos[0] - 2, max_pos[1] - 2


def part_2():
    pass


def main(puzzle_input_f):
    serial_number = int(f.read())

    print("Part 1: ", part_1(serial_number))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    with open("input.txt") as f:

        main(f)
