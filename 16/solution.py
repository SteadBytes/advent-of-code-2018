import re


def addr(A, B, before):
    return before[A] + before[B]


def addi(A, B, before):
    return before[A] + B


def mulr(A, B, before):
    return before[A] * before[B]


def muli(A, B, before):
    return before[A] * B


def banr(A, B, before):
    return before[A] & before[B]


def bani(A, B, before):
    return before[A] & B


def borr(A, B, before):
    return before[A] | before[B]


def bori(A, B, before):
    return before[A] | B


def setr(A, B, before):
    return before[A]


def seti(A, B, before):
    return A


def gtir(A, B, before):
    return int(A > before[B])


def gtri(A, B, before):
    return int(before[A] > B)


def gtrr(A, B, before):
    return int(before[A] > before[B])


def eqir(A, B, before):
    return int(A == before[B])


def eqri(A, B, before):
    return int(before[A] == B)


def eqrr(A, B, before):
    return int(before[A] == before[B])


opcodes = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]

Sample = namedtuple("Sample", ["inst", "before", "after"])


def possible_opcodes(s: Sample):
    A, B, C = s.inst[1:]
    return [opcode for opcode in opcodes if opcode(A, B, s.before) == s.after[C]]


def parse_samples_input(samples_input):
    samples = []
    for sample in samples_input.split("\n\n"):
        before, inst, after = [
            [int(x) for x in re.findall(r"\d+", s)] for s in sample.split("\n")
        ]
        samples.append(Sample(inst, before, after))

    return samples


def part_1(samples):
    possible_ops = [possible_opcodes(s) for s in samples]

    return len([s for s in possible_ops if len(s) >= 3])


def part_2():
    pass


def main(puzzle_input_f):
    samples_input, program_input = puzzle_input_f.read().split("\n\n\n")
    samples = parse_samples_input(samples_input)

    print("Part 1: ", part_1(samples))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
