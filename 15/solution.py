from collections import defaultdict, deque, namedtuple


class Point(namedtuple("Point", ["y", "x"])):
    """ Order of y,x swapped from usual x,y to enable sorting in reading order
    by default
    """

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)

    def adjacent(self):
        vels = [Point(*v) for v in [(-1, 0), (0, -1), (0, 1), (1, 0)]]
        return [self + v for v in vels]


class Unit:
    def __init__(self, pos: Point, team):
        self.pos = pos
        self.team = team
        self.hp = 200
        self.ap = 3

    def __repr__(self):
        return "Unit(team={}, pos={}, hp={}, ap={})".format(
            self.team, self.pos, self.hp, self.ap
        )

    @property
    def alive(self):
        return self.hp > 0


def show_arena(arena):
    y_max = max(p.y for p in arena.keys())
    x_max = max(p.x for p in arena.keys())

    for y in range(y_max + 1):
        l = []
        l_summary = []
        for x in range(x_max + 1):
            e = arena[Point(y, x)]
            if type(e) is bool:
                l.append("#" if e else ".")
            else:
                l.append(e.team)
                l_summary.append(f"{e.team}({e.hp})")
        print("".join(l), ", ".join(l_summary))


def filter_alive(units):
    return [u for u in units if u.alive]


def find_target(unit, elves, goblins):
    enemies = goblins if unit.team == "E" else elves

    in_range = sorted(
        [e for e in filter_alive(enemies) if e.pos in unit.pos.adjacent()],
        key=lambda u: (u.hp, u.pos),
    )

    if in_range:
        return in_range[0]


def find_closest_enemy(unit, arena):
    Q = deque()
    parents = {}
    distances = {}

    for p in unit.pos.adjacent():
        Q.append(p)
        parents[p] = unit.pos
        distances[p] = 1

    closest = None
    while len(Q) > 0:
        p = Q.popleft()
        is_unit = type(arena[p]) == Unit

        if is_unit and arena[p].team != unit.team:
            closest = p
            break

        if is_unit or arena[p] is True:
            continue

        for pt in p.adjacent():
            if pt not in parents:
                parents[pt] = p
                distances[pt] = distances[p] + 1
                Q.append(pt)

    if closest is None:
        return None, None, None

    p = closest
    move = parents[closest]
    while move != unit.pos:
        p = move
        move = parents[p]
    return closest, p, distances[closest]


def do_move(unit, arena):
    closest_enemy, move, distance = find_closest_enemy(unit, arena)

    if move is None or move == unit.pos or distance < 2:
        return

    del arena[unit.pos]
    unit.pos = move
    arena[unit.pos] = unit


def do_round(elves, goblins, arena):

    full_round = True
    for unit in sorted(elves + goblins, key=lambda u: u.pos):
        if not unit.alive:  # died during round
            continue
        if not filter_alive(elves) or not filter_alive(goblins):
            full_round = False
            break
        do_move(unit, arena)
        target_unit = find_target(unit, elves, goblins)
        if target_unit:
            target_unit.hp -= unit.ap
            if not target_unit.alive:
                del arena[target_unit.pos]

    return filter_alive(elves), filter_alive(goblins), arena, full_round


def parse_input(lines):
    elves = []
    goblins = []
    arena = defaultdict(bool)

    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            pt = Point(y, x)
            if ch == "#":
                arena[pt] = True
            elif ch in "GE":
                unit = Unit(pt, ch)
                {"G": goblins, "E": elves}[ch].append(unit)
                arena[pt] = unit
    return elves, goblins, arena


def part_1(lines):
    elves, goblins, arena = parse_input(lines)

    r = 0
    while elves and goblins:
        elves, goblins, arena, full_round = do_round(elves, goblins, arena)
        if full_round:
            r += 1

    hp_sum = sum(u.hp for u in elves + goblins)
    return r * hp_sum


def part_2():
    pass


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1 ", part_1(lines))
    print("Part 2 ", part_2())


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
