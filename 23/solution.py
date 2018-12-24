import re


def extract_ints(s):
    return list(map(int, re.findall(r"-?\d+", s)))


def manhattan(p, q):
    return sum(abs(pi - qi) for pi, qi in zip(p, q))


def part_1(lines):
    nanobots = {(x, y, z): r for x, y, z, r in [extract_ints(l) for l in lines]}

    strongest = max(nanobots, key=nanobots.get)
    r = nanobots[strongest]
    return sum(1 for n in nanobots if manhattan(n, strongest) <= r)


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l for l in puzzle_input_f.read().splitlines() if l]

    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
