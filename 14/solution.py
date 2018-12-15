def part_1(num_recipes):
    recipes_limit = num_recipes + 10
    scoreboard = [3, 7]
    elves = [0, 1]

    while len(scoreboard) < recipes_limit:
        recipe_total = sum(scoreboard[p] for p in elves)
        if recipe_total < 10:
            scoreboard.append(recipe_total)
        else:
            new_scores = divmod(recipe_total, 10)
            scoreboard.extend(new_scores)

        elves = [(p + 1 + scoreboard[p]) % len(scoreboard) for p in elves]
    return "".join(str(x) for x in scoreboard[num_recipes:recipes_limit])


def part_2(num_recipes):
    scoreboard = [3, 7]
    elves = [0, 1]

    score_sequence = [int(s) for s in str(num_recipes)]

    def continue_search():
        return (
            scoreboard[-len(score_sequence) :] != score_sequence
            and scoreboard[-len(score_sequence) - 1 : -1] != score_sequence
        )

    while continue_search():
        recipe_total = sum(scoreboard[p] for p in elves)
        if recipe_total < 10:
            scoreboard.append(recipe_total)
        else:
            new_scores = divmod(recipe_total, 10)
            scoreboard.extend(new_scores)

        elves = [(p + 1 + scoreboard[p]) % len(scoreboard) for p in elves]
    return len(scoreboard) - len(score_sequence) - 1


def main(puzzle_input_f):
    num_recipes = int(puzzle_input_f.readline())

    print("Part 1: ", part_1(num_recipes))
    print("Part 2: ", part_2(num_recipes))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
