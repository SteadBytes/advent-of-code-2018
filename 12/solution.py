def sum_plants(state, initial_state_len):
    offset = (len(state) - initial_state_len) // 2
    return sum(i - offset for i, pot in enumerate(state) if pot)


def gen_state(initial_state, rules):
    current_state = initial_state
    while True:
        current_state = [False] * 4 + current_state + [False] * 4
        next_state = []
        for i in range(2, len(current_state) - 2):
            pattern = current_state[i - 2 : i + 3]
            next_state.append(rules[tuple(pattern)])
        current_state = next_state
        yield current_state


def part_1(initial_state, rules):
    states = gen_state(initial_state, rules)
    state = initial_state
    for _ in range(20):
        state = next(states)

    return sum_plants(state, len(initial_state))


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.read().split("\n") if l]
    initial_state = [ch == "#" for ch in lines[0].split(": ")[1]]
    initial_state_len = len(initial_state)

    rules = {}
    for l in lines[1:]:
        pattern, result = l.split(" => ")
        rules[tuple([ch == "#" for ch in pattern])] = result == "#"

    print("Part 1: ", part_1(initial_state, rules))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
