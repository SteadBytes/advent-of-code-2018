from collections import deque, defaultdict


def play_marbles(n_players, final_marble):
    """
    Play a game of marbles - calculating final scores for each of the elves.

    Returns:
        dict: {elf, score}
    """
    players = defaultdict(int)
    circle = deque([0])
    next_marble = 1
    while True:
        for player in range(n_players):
            if next_marble % 23 == 0:
                players[player] += next_marble
                circle.rotate(7)
                players[player] += circle.pop()
                circle.rotate(-1)
            else:
                circle.rotate(-1)
                circle.append(next_marble)
            next_marble += 1
            if next_marble > final_marble:
                return players


def get_winning_elf_score(n_players, final_marble):
    """
    Play a game of marbles and return the final score of the winning elf.
    """
    scores = play_marbles(n_players, final_marble)
    return max(scores.values())


def part_1(n_players, final_marble):
    return get_winning_elf_score(n_players, final_marble)


def part_2(n_players, final_marble):
    return get_winning_elf_score(n_players, final_marble * 100)


def main(puzzle_input_f):
    l = puzzle_input_f.readline().split()
    n_players, final_marble = int(l[0]), int(l[6])

    print("Part 1: ", part_1(n_players, final_marble))
    print("Part 2: ", part_2(n_players, final_marble))


if __name__ == "__main__":
    # with open("examples.txt") as f:
    #     print("Part 1 examples:\n")
    #     for l in [l.strip().split() for l in f.readlines()]:
    #         n_players, final_marble, answer = int(l[0]), int(l[6]), int(l[11])
    #         print(f"players = {n_players}, final_marble = {final_marble}")
    #         print(f"expected answer = {answer}")
    #         result = get_winning_elf_score(n_players, final_marble)
    #         print(f"answer = {result}")
    #         print(f"{'CORRECT' if result == answer else 'INCORRECT'}")
    #         print()
    with open("input.txt") as f:
        main(f)
