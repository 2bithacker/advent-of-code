#!/usr/bin/env python3

import fileinput

col1 = list()
col2 = list()

if __name__ == "__main__":
    for line in fileinput.input(encoding="utf=8"):
        (num1, num2) = line.split()
        col1.append(int(num1))
        col2.append(int(num2))

    col1.sort()
    col2.sort()

    total = 0

    for x in range(0, len(col1)):
        distance = abs(col1[x] - col2[x])
        total += distance

    print(total)
