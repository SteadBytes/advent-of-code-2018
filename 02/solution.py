from itertools import product


def part_1(box_ids):
    twos = 0
    threes = 0
    for _id in box_ids:
        unique_letters = set(_id)
        freqs = [_id.count(l) for l in unique_letters]
        twos += 1 if [f for f in freqs if f == 2] else 0
        threes += 1 if [f for f in freqs if f == 3] else 0
    return twos * threes


def part_2(box_ids):
    for id_1, id_2 in product(box_ids, box_ids):
        diffs = 0
        for i, chars in enumerate(zip(id_1, id_2)):
            if chars[0] != chars[1]:
                if diffs > 1:
                    break
                else:
                    diffs += 1
        if diffs == 1:
            return id_1[:i] + id_2[i:]


def main(puzzle_input_f):
    box_ids = [l.strip() for l in puzzle_input_f.readlines()]
    print("Part 1:", part_1(box_ids))
    print("Part 2:", part_2(box_ids))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
