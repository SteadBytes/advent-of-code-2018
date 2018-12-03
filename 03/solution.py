import re
from collections import Counter

claim_re = re.compile(
    r"#(?P<_id>[0-9]+) @ "
    r"(?P<left>[0-9]+),(?P<top>[0-9]+): "
    r"(?P<width>[0-9]+)x(?P<height>[0-9]+)"
)


def parse_claim(claim_string):
    m = claim_re.match(claim_string)
    return {k: int(v) for k, v in m.groupdict().items()}


def claim_area(claim):
    return (
        (i, j)
        for i in range(claim["left"], claim["left"] + claim["width"])
        for j in range(claim["top"], claim["top"] + claim["height"])
    )


def part_1(fabric):
    return sum([1 for claim_count in fabric.values() if claim_count > 1])


def part_2(claims, fabric):
    for claim in claims:
        if all(fabric[s] == 1 for s in claim_area(claim)):
            return claim["_id"]


def main(puzzle_input_f):
    claims = [parse_claim(l) for l in puzzle_input_f.readlines()]
    fabric = Counter(s for c in claims for s in claim_area(c))

    print("Part 1: ", part_1(fabric))
    print("Part 2: ", part_2(claims, fabric))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
