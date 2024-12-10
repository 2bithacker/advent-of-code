#!/usr/bin/env python3

import fileinput

if __name__ == "__main__":
    safe_count = 0
    for line in fileinput.input(encoding="utf=8"):
        levels = [int(x) for x in line.split()]
        safe = True
        increasing = levels[0] < levels[1]

        for x in range(0, len(levels) - 1):
            # increasing, but next number is lower
            if increasing and levels[x] > levels[x + 1]:
                safe = False
                break
            # decreasing, but next number is higher
            if not increasing and levels[x] < levels[x + 1]:
                safe = False
                break
            # difference <1 or >3
            if not (0 < abs(levels[x] - levels[x + 1]) < 4):
                safe = False
                break
        if safe:
            safe_count += 1

    print(safe_count)
