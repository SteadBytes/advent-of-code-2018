import string

unit_pairs_map = {
    **{ch: ch.upper() for ch in string.ascii_lowercase},
    **{ch: ch.lower() for ch in string.ascii_uppercase},
}


def react_polymer(polymer):
    stack = []
    for unit in polymer:
        if stack and unit == unit_pairs_map[stack[-1]]:
            stack.pop()
        else:
            stack.append(unit)
    return stack


def part_1(polymer):
    return len(react_polymer(polymer))


def part_2(polymer):
    best = len(polymer)
    for ch in string.ascii_lowercase:
        reacted_polymer = react_polymer(
            [u for u in polymer if u != ch and u != ch.upper()]
        )
        best = min(best, len(reacted_polymer))
    return best


def main(puzzle_input_f):
    polymer = puzzle_input_f.read().strip()
    print("Original length: ", len(polymer))
    print("Part 1: ", part_1(polymer))
    print("Part 2: ", part_2(polymer))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
