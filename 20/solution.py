from collections import defaultdict, namedtuple


class Point(namedtuple("Point", ["x", "y"])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


Node = namedtuple("Node", ["pt", "dist"])


def build_facility_map(regex):
    # DFS to build map of rooms -> dists
    directions = {
        "N": Point(0, -1),
        "S": Point(0, 1),
        "E": Point(1, 0),
        "W": Point(-1, 0),
    }

    m = defaultdict(lambda: float("inf"))
    current = Node(Point(0, 0), 0)
    s = [current]

    for ch in regex[1:-1]:  # skip start and end anchors
        if ch in directions:
            pt = current.pt + directions[ch]
            dist = min(m[pt], current.dist + 1)
            node = Node(pt, dist)
            current = node
            m[node.pt] = node.dist
        elif ch == "(":
            s.append(current)
            pass
        elif ch == ")":
            current = s.pop()
        elif ch == "|":
            current = s[-1]
    return m


def part_1(facility_map):
    return max(facility_map.values())


def part_2(facility_map):
    return len([d for d in facility_map.values() if d >= 1000])


def main(puzzle_input_f):
    regex = puzzle_input_f.read().strip()
    facility_map = build_facility_map(regex)

    print("Part 1: ", part_1(facility_map))
    print("Part 2: ", part_2(facility_map))


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
