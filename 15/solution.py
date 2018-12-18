from enum import Enum
from collections import namedtuple, deque
from pprint import pprint


class UnitType(Enum):
    ELF = 1
    GOBLIN = 2


class NoTargetsException(Exception):
    pass


Point = namedtuple("Point", ["x", "y"])


class Unit:
    def __init__(self, unit_type: UnitType, position: Point):
        self.unit_type = unit_type
        self.position = position

        self.hp = 200
        self.ap = 3

    def __repr__(self):
        return "Unit(unit_type={}, position={}, hp={}, ap={})".format(
            self.unit_type.name, self.position, self.hp, self.ap
        )

    @property
    def alive(self):
        return self.hp > 0


def adj_points(p: Point):
    vels = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return (Point(p.x + vx, p.y + vy) for vx, vy in vels)


def part_1():
    pass


def part_2():
    pass


def reading_order(p: Point):
    return (p.y, p.x)


def print_grid(grid, units):
    alive = [u for u in units if u.alive]
    prev_y = 0
    line = []

    def output_line():
        units_on_line = sorted(
            [u for u in alive if u.position.y == prev_y], key=lambda u: u.position.x
        )
        unit_summary = [
            "{}({})".format("E" if u.unit_type == UnitType.ELF else "G", u.hp)
            for u in units_on_line
        ]
        print("".join(line) + "\t" + ", ".join(unit_summary))

    for pos in sorted(grid, key=reading_order):
        if prev_y != pos.y:
            output_line()
            line = []
        unit_at_pos = [u for u in alive if u.position == pos]
        if unit_at_pos:
            unit = unit_at_pos[0]
            line.append("E" if unit.unit_type == UnitType.ELF else "G")
        else:
            wall = grid[pos]
            line.append("#" if wall else ".")
        prev_y = pos.y
    output_line()


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    # parse input into list of units and dict representing grid
    units = []

    grid = {}

    char_unit_types = {"E": UnitType.ELF, "G": UnitType.GOBLIN}
    for i, row in enumerate(lines):
        for j, ch in enumerate(row):
            grid[Point(i, j)] = ch == "#"

            if ch in char_unit_types:
                unit_type = char_unit_types[ch]
                units.append(Unit(unit_type, Point(i, j)))

    def find_move(unit: Unit, targets):
        # BFS
        QueueItem = namedtuple("QueueItem", ["pos", "dist"])
        PositionInfo = namedtuple("PositionInfo", ["dist", "parent"])

        Q = deque([QueueItem(unit.position, 0)])
        position_info = {unit.position: PositionInfo(0, None)}
        visited = set()
        occupied_positions = {u.position for u in units if u.alive}

        while Q:
            curr = Q.popleft()
            for p in adj_points(curr.pos):
                if grid[p] or p in occupied_positions:
                    continue
                p_dist = curr.dist + 1
                current_best = position_info.get(p)
                curr_info = PositionInfo(p_dist, curr.pos)
                if not current_best or current_best > curr_info:
                    position_info[p] = curr_info

                if p in visited:
                    continue

                if not any(p == v.pos for v in Q):
                    Q.append(QueueItem(p, p_dist))
            visited.add(curr.pos)

        try:
            min_dist, closest = min(
                (pi.dist, pos) for pos, pi in position_info.items() if pos in targets
            )
        except ValueError:
            return

        while position_info[closest].dist > 1:
            closest = position_info[closest].parent

        return closest

    def move(unit: Unit):
        targets = [u for u in units if unit.unit_type != u.unit_type and u.alive]
        if not targets:
            raise NoTargetsException

        occupied_positions = {u.position for u in units if u.alive and u != unit}

        in_range = {
            p
            for t in targets
            for p in adj_points(t.position)
            if p not in occupied_positions and not grid[p]
        }
        if unit.position not in in_range:
            move = find_move(unit, in_range)
            if move:
                unit.position = move

        enemies = [t for t in targets if t.position in adj_points(unit.position)]
        if enemies:
            chosen = min(enemies, key=lambda u: (u.hp, reading_order(u.position)))
            chosen.hp -= unit.ap

    def simulate_round():
        alive = [u for u in units if u.alive]
        for unit in sorted(alive, key=lambda u: reading_order(u.position)):
            move(unit)

    rounds = 0
    while True:
        print_grid(grid, units)
        print()
        try:
            simulate_round()
        except NoTargetsException:
            break
        rounds += 1

    print(rounds)
    print(rounds * sum(u.hp for u in units if u.alive))

    print("Part 1: ", part_1())
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
