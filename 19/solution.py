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


def sum_factors(n):
    return sum(
        {x for i in range(1, int(n ** 0.5) + 1) if n % i == 0 for x in (i, n // i)}
    )


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


def part_1(ip_reg, instructions, simulate=True, verbose=False):
    """ Program calculates the sum of the factors of a number. The number is
    stored in register 5 and is calculated during a 'setup' phase. For part 1,
    this value is 981.

    The main algorithm of the program converted to Python:
    ```
    n = 981
    r = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i * j == n:
                r += 1
    return r
    ```

    When simulate=True, the program is simulated by running
    the instructions against an in-memory register and returning the result
    from register 0.

    When simulate=False, the sum_factors python function is called to produce
    the answer without simulating the program.
    """
    if simulate:
        return simulate_program(ip_reg, instructions, verbose=verbose)
    else:
        return sum_factors(981)


def part_2():
    """ Setting register 0 to 1 acts as a flag to use a 10551381 as the value
    to calculate the sum of factors for. The program implements this very
    naively and as such will take a very long time to complete.
    """
    return sum_factors(10_551_381)


def main(puzzle_input_f):
    ip_reg = int(puzzle_input_f.readline().split()[1])
    instructions = [
        (l.split()[0], [int(x) for x in l.split()[1:]])
        for l in puzzle_input_f.read().splitlines()
    ]

    print("Part 1: ", part_1(ip_reg, instructions, simulate=True))
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
