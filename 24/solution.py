import re
from dataclasses import dataclass, field


@dataclass
class Group:
    id: int
    units: int
    hp: int
    ap: int
    attack_type: str
    initiative: int
    team: str
    weak_to: set = field(default_factory=set)
    immune_to: set = field(default_factory=set)

    @property
    def ep(self):
        return self.units * self.ap

    @property
    def global_id(self):
        return f"{self.team}-{self.id}"


GROUP_RE = re.compile(
    r"(?P<units>\d+) units each with (?P<hp>\d+) hit points "
    r"(?P<damage_info>\([^)]*\) )?with an attack that does (?P<ap>\d+) "
    r"(?P<attack_type>\w+) damage at initiative (?P<initiative>\d+)"
)


def parse_group(group_input, group_num, team):
    m = GROUP_RE.search(group_input).groupdict()
    damage_info = m.pop("damage_info", None)

    group = Group(
        group_num,
        int(m["units"]),
        int(m["hp"]),
        int(m["ap"]),
        m["attack_type"],
        int(m["initiative"]),
        team,
    )

    if damage_info:
        for info in damage_info.strip()[1:-1].split("; "):
            if "weak" in info:
                group.weak_to.update(
                    s.strip() for s in info.split("weak to ")[1].split(",")
                ),
            elif "immune" in info:
                group.immune_to.update(
                    s.strip() for s in info.split("immune to ")[1].split(",")
                ),

    return group


def parse_input(s):
    team_inputs = [t.splitlines()[1:] for t in s.split("\n\n")]
    immune_system = [
        parse_group(g, i, "immune_sys") for i, g in enumerate(team_inputs[0])
    ]
    infection = [parse_group(g, i, "infection") for i, g in enumerate(team_inputs[1])]
    return immune_system, infection


def calc_damage(g: Group, target: Group):
    if g.attack_type in target.immune_to:
        return 0
    return 2 * g.ep if g.attack_type in target.weak_to else g.ep


def choose_target(g: Group, targets):
    def target_sort(t):
        return (-calc_damage(g, t), -t.ep, -t.initiative)

    return sorted(targets, key=target_sort)[0]


def print_attacks(attacks):
    headers = ["Attacker", "Defender", "Damage", "Killed"]
    out = [headers] + attacks
    for i, d in enumerate(out):
        line = "|".join(str(x).ljust(15) for x in d)
        print(line)
        if i == 0:
            print("-" * len(line))


def do_round(immune_sys, infection, verbose=False):
    fights = {}
    targeted = set()
    groups = immune_sys + infection

    for g in sorted(groups, key=lambda g: (-g.ep, -g.initiative)):
        enemies = [e for e in groups if g.team != e.team]
        targets = [e for e in enemies if e.global_id not in targeted]
        if targets:
            target = choose_target(g, targets)
            targeted.add(target.global_id)
            fights[g.global_id] = target

    if verbose:
        attacks = []

    for g in sorted(groups, key=lambda g: -g.initiative):
        if g.global_id not in fights:
            continue
        target = fights[g.global_id]
        damage = calc_damage(g, target)
        killed = min(target.units, damage // target.hp)
        target.units -= killed

        if verbose:
            attacks.append([g.global_id, target.global_id, damage, killed])

    if verbose:
        print_attacks(attacks)
        print()

    immune_sys = [g for g in immune_sys if g.units > 0]
    infection = [g for g in infection if g.units > 0]

    return immune_sys, infection


def part_1(immune_sys, infection):
    while True:
        immune_sys, infection = do_round(immune_sys, infection)
        immune_sys_units = sum(g.units for g in immune_sys)
        infection_units = sum(g.units for g in infection)

        if immune_sys_units == 0:
            return infection_units
        if infection_units == 0:
            return immune_sys_units


def part_2():
    pass


def main(puzzle_input_f):
    verbose = False
    immune_sys, infection = parse_input(puzzle_input_f.read())
    print("Part 1: ", part_1(immune_sys, infection))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    main(input_cli(base_dir))
