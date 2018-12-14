from collections import defaultdict


class Cart:
    turn_order = {"L": "F", "F": "R", "R": "L"}

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.next_turn = "L"

    def __str__(self):
        return f"({self.position}, {self.direction})"

    def __repr__(self):
        return f"Cart(position={self.position}, direction={self.direction})"

    def turn(self, track):
        if not track:
            return
        if track == "\\":
            if self.direction.real == 0:
                self.turn_counter_clockwise()
            else:
                self.turn_clockwise()
        elif track == "/":
            if self.direction.real == 0:
                self.turn_clockwise()
            else:
                self.turn_counter_clockwise()
        elif track == "+":
            turn = self.next_turn
            self.next_turn = self.turn_order[turn]
            if turn == "L":
                self.turn_counter_clockwise()
            elif turn == "R":
                self.turn_clockwise()

    def turn_clockwise(self):
        self.direction *= 1j

    def turn_counter_clockwise(self):
        self.direction *= -1j


def part_1(carts, tracks):
    while True:
        carts.sort(key=lambda cart: (cart.position.imag, cart.position.real))
        for cart in carts:
            cart.position += cart.direction
            if any(cart2.position == cart.position for cart2 in carts if cart != cart2):
                return (int(cart.position.real), int(cart.position.imag))
            track = tracks[cart.position]
            cart.turn(track)


def part_2():
    pass


def init_carts_and_tracks(input_lines):
cart_directions = {"<": -1, "v": +1j, ">": 1, "^": -1j}
cart_tracks = {"<": "-", "v": "|", ">": "-", "^": "|"}

    tracks = defaultdict(str)
    carts = []

    for y, row in enumerate(input_lines):
        for x, ch in enumerate(row):
            pos = x + y * 1j
            if ch in cart_directions:
                direction = cart_directions[ch]
                carts.append(Cart(pos, direction))
                track = cart_tracks[ch]
            else:
                track = ch
            if track in "\\/+":
                tracks[(pos)] = track

    return carts, tracks


def main(puzzle_input_f):
    lines = puzzle_input_f.readlines()
    print("Part 1: ", part_1(*init_carts_and_tracks(lines)))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
