def part_1(entries):
    """
    Basic premise:
    header = n_child, n_meta
    n_child == 0 -> meta_total = sum(entries[:n_meta])
    n_child > 0 -> meta_total = sum(children_meta_totals) + current_meta_total

    1. Get header items from entries
    2. Remove header items from entries and start meta_total at 0
    3. For each child recursively call function with remaining entries, update
        meta_total with returned value
    4. Update meta_total with current node meta_total (i.e. n_child == 0 case)
    5. return meta_total, remaining_entries
    """

    def sum_metadata(entries):
        n_child, n_meta = entries[:2]
        remaining_entries = entries[2:]

        meta_total = 0

        for _ in range(n_child):
            child_total, remaining_entries = sum_metadata(remaining_entries)
            meta_total += child_total

        meta_total += sum(remaining_entries[:n_meta])

        return meta_total, remaining_entries[n_meta:]

    return sum_metadata(entries)[0]


def part_2(entries):
    pass


def main(puzzle_input_f):
    entries = [int(e) for e in puzzle_input_f.read().split()]
    print("Part 1: ", part_1(entries))
    print("Part 2: ", part_2(entries))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
