import os
import re
from collections import defaultdict

id_re = re.compile(r"#(\d+)")


def parse_minute(record):
    timestamp, action = record.split("] ")
    return int(timestamp.split(":")[1])


def parse_id(record):
    m = id_re.search(record)
    return int(m.group(1)) if m is not None else None


def process_records(records, on_wake_up):
    current_guard = None
    asleep_minute = None
    for r in records:
        if not r:
            continue
        minute = parse_minute(r)
        if "begins shift" in r:
            current_guard = parse_id(r)
            asleep_minute = None
        elif "falls asleep" in r:
            asleep_minute = minute
        elif "wakes up" in r:
            on_wake_up(current_guard, range(asleep_minute, minute))


def part_1(records):
    guard_minute_asleep_counts = defaultdict(lambda: defaultdict(int))
    guards_asleep_totals = defaultdict(int)

    def on_wake_up(current_guard, asleep_minutes_range):
        for m in asleep_minutes_range:
            guard_minute_asleep_counts[current_guard][m] += 1
            guards_asleep_totals[current_guard] += 1

    process_records(records, on_wake_up)

    most_asleep_guard = max(guards_asleep_totals, key=guards_asleep_totals.get)
    most_asleep_minute = max(
        guard_minute_asleep_counts[most_asleep_guard],
        key=guard_minute_asleep_counts[most_asleep_guard].get,
    )
    return most_asleep_guard * most_asleep_minute


def part_2(records):
    guard_minute_asleep_counts = defaultdict(int)

    def on_wake_up(current_guard, asleep_minutes_range):
        for m in asleep_minutes_range:
            guard_minute_asleep_counts[(current_guard, m)] += 1

    process_records(records, on_wake_up)

    guard_id, minute = max(
        guard_minute_asleep_counts, key=guard_minute_asleep_counts.get
    )
    return guard_id * minute


def main(puzzle_input_f):
    records = puzzle_input_f.read().splitlines()
    records.sort()

    print("Part 1: ", part_1(records))
    print("Part 2: ", part_2(records))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
