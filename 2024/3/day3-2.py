#!/usr/bin/env python3

import fileinput
import re

if __name__ == "__main__":
    total = 0
    enabled = True
    for line in fileinput.input(encoding="utf=8"):
        matches = re.findall(r"(do(?:n't)?|mul)\((?:(\d+),(\d+)|)\)", line)
        for command, x, y in matches:
            match command:
                case "do":
                    enabled = True
                case "don't":
                    enabled = False
                case "mul":
                    if enabled:
                        total += int(x) * int(y)

    print(total)
