#!/usr/bin/env python3

import fileinput
import pprint

col1 = list()
col2 = list()

if __name__ == "__main__":
    for line in fileinput.input(encoding="utf=8"):
        (num1,num2) = line.split()
        col1.append(int(num1))
        col2.append(int(num2))

    total = 0

    for x in range(0, len(col1)):
        score = col1[x] * col2.count(col1[x])
        total += score

    print(total)
