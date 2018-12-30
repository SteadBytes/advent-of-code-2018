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


def gtri(A, B, before):
    """ Reg C -> 1 if reg A > val B else 0
    """
    return int(before[A] > B)


def gtrr(A, B, before):
    """ Reg C -> 1 if reg A > reg B else 0
    """
    return int(before[A] > before[B])


def eqir(A, B, before):
    """ Reg C -> 1 if val A == reg B else 0
    """
    return int(A == before[B])


def eqri(A, B, before):
    """ Reg C -> 1 if reg A == val B else 0
    """
    return int(before[A] == B)


def eqrr(A, B, before):
    """ Reg C -> 1 if reg A == reg B else 0
    """
    return int(before[A] == before[B])


opcodes = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "band": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}


def simulate_program(ip_reg, instructions, r0=0, verbose=False):
    r = [0] * 6
    r[0] = r0
    r[ip_reg] = 0
    ip = 0
    while ip < len(instructions):
        opcode, (A, B, C) = instructions[ip]
        r[ip_reg] = ip

        if verbose:
            l = f"ip={ip} {r} {opcode} {A} {B} {C}"

        r[C] = opcodes[opcode](A, B, r)
        ip = r[ip_reg]
        ip += 1
        if verbose:
            print(f"{l} {r}")
    return r[0]


def program(part_1=True):
    """ Reverse engineered from Elf code source with additions for solving the
    puzzles.
    """
    r3 = 0
    prev_halt_r3 = 0
    s = set()
    while True:
        r4 = r3 | 65536
        r3 = 1_107_552
        while True:
            r5 = r4 & 255
            r3 += r5
            r3 &= 16_777_215
            r3 *= 65899
            r3 &= 16_777_215
            if 256 > r4:
                if part_1:
                    return r3
                else:
                    # track values of r3 that would cause halt
                    # when no more values added the previous value that caused
                    # a halt will be the value that causes the most instructions
                    # to be executed
                    prev_s = {x for x in s}
                    s.add(r3)
                    prev_halt_r3 = prev_halt_r3 if r3 in prev_s else r3
                    if prev_s == s:
                        return prev_halt_r3
                    break
            r4 = r4 // 256  # additional optimisation


def part_1():
    return program()


def part_2():
    return program(part_1=False)


def main(puzzle_input_f):
    ip_reg = int(puzzle_input_f.readline().split()[1])
    instructions = [
        (l.split()[0], [int(x) for x in l.split()[1:]])
        for l in puzzle_input_f.read().splitlines()
    ]

    print("Part 1: ", part_1())
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)
