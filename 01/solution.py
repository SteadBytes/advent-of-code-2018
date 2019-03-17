def parse_frequencies(puzzle_input):
    return [int(f) for f in puzzle_input.readlines()]


def part_1(frequencies):
    return sum(frequencies)


def part_2(frequencies):
    frequency_memo = {0}
    current_frequency = 0
    while True:
        for f in frequencies:
            current_frequency += f
            if current_frequency in frequency_memo:
                return current_frequency
            frequency_memo.add(current_frequency)


def main(puzzle_input_f):
    frequencies = parse_frequencies(puzzle_input_f)
    print("Part 1:", part_1(frequencies))
    print("Part 2:", part_2(frequencies))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
