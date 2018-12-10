import re


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


def main(puzzle_input_f):
    lines = puzzle_input_f.readlines()
    values = [[int(x) for x in re.findall(r"-?\d+", l)] for l in lines]
    points = [Point(x, y, vx, vy) for x, y, vx, vy in values]

    prev_size = float("inf")
    time = 0
    while True:
        m = set()
        x_min = y_min = float("inf")
        x_max = y_max = 0
        for p in points:
            m.add((p.x, p.y))
            x_min = min(x_min, p.x)
            x_max = max(x_max, p.x)
            y_min = min(y_min, p.y)
            y_max = max(y_max, p.y)

        size = x_max - x_min + y_max - y_min
        # I ran first with this uncommented and if size == 70 commented to find
        # correct size to stop at. Then ran with the if size == 70 to print
        # the output
        # also answers part two
        # if size > prev_size:
        #   print(time - 1, prev_size - 1)
        #   break
        if size == 70:
            for y in range(y_min, y_max + 1):
                l = ["#" if (x, y) in m else "." for x in range(x_min, x_max + 1)]
                print("".join(l))
            break

        prev_size = size
        time += 1

        for p in points:
            p.x += p.vx
            p.y += p.vy


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
