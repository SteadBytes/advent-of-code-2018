from collections import deque


def manhattan(p, q):
    return sum(abs(pi - qi) for pi, qi in zip(p, q))


def part_1(points):
    in_range = [set() for _ in range(len(points))]
    for p1_index, p1 in enumerate(points):
        for p2_index, p2 in enumerate(points):
            if manhattan(p1, p2) <= 3:
                in_range[p1_index].add(p2_index)

    constellations = 0
    part_of_constellation = set()

    for p1_index in range(len(points)):
        if p1_index in part_of_constellation:
            continue
        constellations += 1
        queue = deque([p1_index])
        while queue:
            p2_index = queue.popleft()
            if p2_index in part_of_constellation:
                continue
            part_of_constellation.add(p2_index)
            p2_in_range = in_range[p2_index]
            queue.extend(p2_in_range)
    return constellations


def part_2():
    pass


def parse_points(lines):
    return [tuple(map(int, l.split(","))) for l in lines]


def test_example_inputs(puzzle_input_f):
    for i, example in enumerate(puzzle_input_f.read().split("\n\n")):
        lines = [l.strip() for l in example.split("\n") if l]
        expected = int(lines.pop())
        points = parse_points(lines)
        result = part_1(points)
        try:
            assert result == expected
        except AssertionError:
            print(f"Ex {i} incorrect: expected {expected}, got {result}")


def main(puzzle_input_f):
    # puzzle gave multiple example inputs and results
    # example_input.txt contains each input follwed by the result
    # inputs/results separated by blank line
    if puzzle_input_f.name == "example_input.txt":
        test_example_inputs(puzzle_input_f)
        return

    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    points = parse_points(lines)

    print("Part 1: ", part_1(points))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
