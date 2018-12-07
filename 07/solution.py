import re
from collections import defaultdict


def find_next_steps(steps, prereq_step_pairs):
    next_steps = sorted(
        [step for step in steps if all(s != step for prereq, s in prereq_step_pairs)]
    )
    return next_steps


def part_1(lines):
    prereq_step_pairs = [re.findall(r"step (\w) ", l, re.IGNORECASE) for l in lines]

    steps = {s for steps in prereq_step_pairs for s in steps}

    step_order = []
    while steps:
        next_step = find_next_steps(steps, prereq_step_pairs)[0]
        step_order.append(next_step)
        steps.remove(next_step)
        prereq_step_pairs = [
            (prereq, s) for (prereq, s) in prereq_step_pairs if prereq != next_step
        ]

    return "".join(step_order)


def calculate_step_time(s):
    return (ord(s) - ord("A") + 1) + 60


def part_2(lines):
    prereq_step_pairs = [re.findall(r"step (\w) ", l, re.IGNORECASE) for l in lines]

    steps = {s for steps in prereq_step_pairs for s in steps}

    time = -1
    workers = [{"step": None, "time": 0} for _ in range(5)]
    while steps or any(w["time"] > 0 for w in workers):
        for w in workers:
            w["time"] = max(w["time"] - 1, 0)

            if w["time"] == 0:
                if w["step"] is not None:
                    prereq_step_pairs = [
                        (prereq, s)
                        for (prereq, s) in prereq_step_pairs
                        if prereq != w["step"]
                    ]
                    w["step"] = None
                next_steps = find_next_steps(steps, prereq_step_pairs)
                if next_steps:
                    step = next_steps.pop()
                    w["time"] = calculate_step_time(step)
                    w["step"] = step
                    steps.remove(step)
        time += 1
    return time


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines()]
    print("Part 1: ", part_1(lines))
    print("Part 2: ", part_2(lines))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
