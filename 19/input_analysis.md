`#ip 3`

| i   | Opcode | A   | B   | C   |
| --- | ------ | --- | --- | --- |
| 0   | addi   | 3   | 16  | 3   |
| 1   | seti   | 1   | 0   | 4   |
| 2   | seti   | 1   | 7   | 2   |
| 3   | mulr   | 4   | 2   | 1   |
| 4   | eqrr   | 1   | 5   | 1   |
| 5   | addr   | 1   | 3   | 3   |
| 6   | addi   | 3   | 1   | 3   |
| 7   | addr   | 4   | 0   | 0   |
| 8   | addi   | 2   | 1   | 2   |
| 9   | gtrr   | 2   | 5   | 1   |
| 10  | addr   | 3   | 1   | 3   |
| 11  | seti   | 2   | 6   | 3   |
| 12  | addi   | 4   | 1   | 4   |
| 13  | gtrr   | 4   | 5   | 1   |
| 14  | addr   | 1   | 3   | 3   |
| 15  | seti   | 1   | 3   | 3   |
| 16  | mulr   | 3   | 3   | 3   |
| 17  | addi   | 5   | 2   | 5   |
| 18  | mulr   | 5   | 5   | 5   |
| 19  | mulr   | 3   | 5   | 5   |
| 20  | muli   | 5   | 11  | 5   |
| 21  | addi   | 1   | 6   | 1   |
| 22  | mulr   | 1   | 3   | 1   |
| 23  | addi   | 1   | 13  | 1   |
| 24  | addr   | 5   | 1   | 5   |
| 25  | addr   | 3   | 0   | 3   |
| 26  | seti   | 0   | 6   | 3   |
| 27  | setr   | 3   | 1   | 1   |
| 28  | mulr   | 1   | 3   | 1   |
| 29  | addr   | 3   | 1   | 1   |
| 30  | mulr   | 3   | 1   | 1   |
| 31  | muli   | 1   | 14  | 1   |
| 32  | mulr   | 1   | 3   | 1   |
| 33  | addr   | 5   | 1   | 5   |
| 34  | seti   | 0   | 0   | 0   |
| 35  | seti   | 0   | 3   | 3   |

```
i0 = JMP 17

i1->i16 = MAIN
  i2->i15 = LOOP1
  i3->i11 = LOOP2
i16 = HALT

i17->i26 = SETUP P1
i17 -> i35 = SETUP P2
```

## `SETUP`

```
| 17  | addi   | 5   | 2   | 5   | SETUP
| 18  | mulr   | 5   | 5   | 5   | r5 = 981 |
| 19  | mulr   | 3   | 5   | 5   | --> r5 = 2 \*_ 2 _ 19 \* 11 = 836 |
| 20  | muli   | 5   | 11  | 5   | r1 = 6 \* 22 + 13 145 |
| 21  | addi   | 1   | 6   | 1   | r5 += r1 = 981 |
| 22  | mulr   | 1   | 3   | 1   |
| 23  | addi   | 1   | 13  | 1   |
| 24  | addr   | 5   | 1   | 5   |
| 25  | addr   | 3   | 0   | 3   | -> if R0 == 0: (flag for part1/part2) |
| 26  | seti   | 0   | 6   | 3   | ---> JMP 1 |
| 27  | setr   | 3   | 1   | 1   | PART 2 continue setup to start with larger number |
| 28  | mulr   | 1   | 3   | 1   | r5 = 10551381 |
| 29  | addr   | 3   | 1   | 1   | --> rr = (27 _ 28 +29) _ 30 _ 14 _ 32 = 10550400 |
| 30  | mulr   | 3   | 1   | 1   | r5 += r1 = 981 + 10550400 = 10551381 |
| 31  | muli   | 1   | 14  | 1   |
| 32  | mulr   | 1   | 3   | 1   |
| 33  | addr   | 5   | 1   | 5   |
| 34  | seti   | 0   | 0   | 0   |
| 35  | seti   | 0   | 3   | 3   |
```

## `MAIN`

```
| 2   | seti   | 1   | 7   | 2   | LOOP1 r2 = 1 |
| 3   | mulr   | 4   | 2   | 1   | LOOP2 |
| 4   | eqrr   | 1   | 5   | 1   |
| 5   | addr   | 1   | 3   | 3   | if (r4 \* r2) == r5 |
| 6   | addi   | 3   | 1   | 3   | r0 += r4 |
| 7   | addr   | 4   | 0   | 0   | -------------------- |
| 8   | addi   | 2   | 1   | 2   | r2 +=1 |
| 9   | gtrr   | 2   | 5   | 1   | -------------------- |
| 10  | addr   | 3   | 1   | 3   | if (if r2 <= r5) |
| 11  | seti   | 2   | 6   | 3   | jmp 3 -> (LOOP2) |
| 12  | addi   | 4   | 1   | 4   | -------------------- |
| 13  | gtrr   | 4   | 5   | 1   |
| 14  | addr   | 1   | 3   | 3   |
| 15  | seti   | 1   | 3   | 3   |
| 16  | mulr   | 3   | 3   | 3   | HALT |
```

## Algorithm

```Python
n = 981 if part1 else 10551381
r = 0
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if i * j == n:
            r += 1
return r
```
