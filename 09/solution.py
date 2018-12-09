def part_1(n_players, final_marble):
    """
    start w/ marble 0 -> current marble
     elf take turn placing lowest numbered remaining marble
     -> between marbles 1 and 2 clockwise of current marble
     -> marble placed = current marble
     if marble is multiple of 23
     current player keeps marble -> add to score
     marble 7 marbles counter-clockwise from current removed -> add to score
     marble immediately clockwise of removed = current marble

     Players -> list of lists of marbles each player 'owns'
     Circle -> list of marbles (values)
     Remaining marbles -> int counter (stop when counter == final_marble score)
     -> increment each time to get next lowest remaining
    """
    players = [[] for _ in range(n_players)]
    circle = [0]
    next_marble = 1
    current_marble_i = 0

    while True:
        for p in players:
            if next_marble % 23 == 0:
                p.append(next_marble)
                to_remove_i = (current_marble_i - 7) % len(circle)
                removed = circle.pop(to_remove_i)
                p.append(removed)
                current_marble_i = to_remove_i
            else:
                i1, i2 = [(current_marble_i + i) % len(circle) for i in range(1, 3)]
                if i2 == 0:
                    circle.append(next_marble)
                    current_marble_i = len(circle) - 1
                else:
                    circle = circle[: i1 + 1] + [next_marble] + circle[i2:]
                    current_marble_i = i1 + 1
            next_marble += 1
            if next_marble > final_marble:
                return max([sum(p) for p in players])


def part_2():
    pass


def main(puzzle_input_f):
    l = puzzle_input_f.readline().split()
    n_players, final_marble = int(l[0]), int(l[6])

    print("Part 1: ", part_1(n_players, final_marble))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    with open("examples.txt") as f:
        print("Part 1 examples:\n")
        for l in [l.strip().split() for l in f.readlines()]:
            n_players, final_marble, answer = int(l[0]), int(l[6]), int(l[11])
            print(f"players = {n_players}, final_marble = {final_marble}")
            print(f"expected answer = {answer}")
            result = part_1(n_players, final_marble)
            print(f"answer = {result}")
            print(f"{'CORRECT' if result == answer else 'INCORRECT'}")
            print()
    with open("input.txt") as f:
        main(f)
