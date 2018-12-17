import re
from collections import defaultdict, namedtuple


def addr(A, B, before):
    """ Reg C -> result of adding reg A and reg B
    """
    return before[A] + before[B]


def addi(A, B, before):
    """ Reg C -> result of adding reg A and val B
    """
    return before[A] + B


def mulr(A, B, before):
    """ Reg C -> result of multiplying reg A and reg B
    """
    return before[A] * before[B]


def muli(A, B, before):
    """ Reg C -> result of multiplying reg A and val B
    """
    return before[A] * B


def banr(A, B, before):
    """ Reg C -> result of bitwise AND reg A and reg B
    """
    return before[A] & before[B]


def bani(A, B, before):
    """ Reg C -> result of bitwise AND reg A and val B
    """
    return before[A] & B


def borr(A, B, before):
    """ Reg C -> result of bitwise OR reg A and reg B
    """
    return before[A] | before[B]


def bori(A, B, before):
    """ Reg C -> result of bitwose OR reg A and val B
    """
    return before[A] | B


def setr(A, B, before):
    """ Reg C -> contents of reg A (input B ignored)
    """
    return before[A]


def seti(A, B, before):
    """ Reg C -> val A (input B ignored)
    """
    return A


def gtir(A, B, before):
    """ Reg C -> 1 if val A > reg B else 0
    """
    return int(A > before[B])


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


def parse_program_input(program_input):
    lines = (l for l in program_input.split("\n") if l)
    return [[int(x) for x in l.strip().split()] for l in lines]


def part_1(samples):
    possible_ops = [possible_opcodes(s) for s in samples]

    return len([s for s in possible_ops if len(s) >= 3])


def part_2(samples, program):
    possible_ops = defaultdict(lambda: set(opcodes))
    for s in samples:
        op_num = s.inst[0]
        possible_ops[op_num] &= set(possible_opcodes(s))

    op_num_map = {}
    while any(possible_ops.values()):
        known = [op_num for op_num, ops in possible_ops.items() if len(ops) == 1]

        for op_num in known:
            op_num_map[op_num] = op = possible_ops[op_num].pop()
            for possible in possible_ops.values():
                possible.discard(op)

    registers = [0] * 4
    for op_num, A, B, C in program:
        registers[C] = op_num_map[op_num](A, B, registers)

    return registers[0]


def main(puzzle_input_f):
    samples_input, program_input = puzzle_input_f.read().split("\n\n\n")
    samples = parse_samples_input(samples_input)
    program = parse_program_input(program_input)

    print("Part 1: ", part_1(samples))
    print("Part 2: ", part_2(samples, program))


if __name__ == "__main__":
    with open("input.txt") as f:
        main(f)
