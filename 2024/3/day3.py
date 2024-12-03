#!/usr/bin/env python3

import fileinput
import re

if __name__ == "__main__":
    total = 0
    for line in fileinput.input(encoding="utf=8"):
        matches = re.findall(r"mul\((\d+),(\d+)\)", line)
        for x, y in matches:
            product = int(x) * int(y)
            total += product

    print(total)
