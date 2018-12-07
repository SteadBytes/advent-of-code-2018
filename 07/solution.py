import re
from collections import defaultdict


def find_next_step(steps, prereq_step_pairs):
    next_steps = sorted(
        [step for step in steps if all(s != step for prereq, s in prereq_step_pairs)]
    )
    return next_steps[0]


def part_1(lines):
    prereq_step_pairs = [re.findall(r"step (\w) ", l, re.IGNORECASE) for l in lines]

    steps = {s for steps in prereq_step_pairs for s in steps}

    step_order = []
    while steps:
        next_step = find_next_step(steps, prereq_step_pairs)
        step_order.append(next_step)
        steps.remove(next_step)
        prereq_step_pairs = [
            (prereq, s) for (prereq, s) in prereq_step_pairs if prereq != next_step
        ]

    return "".join(step_order)


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines()]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
