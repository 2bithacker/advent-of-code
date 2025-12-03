#!/usr/bin/env python3

import fileinput


class BatteryBank(object):
    def __init__(self, cells: list):
        self.cells = cells

    def max_joltage(self, n=12) -> int:
        value = 0
        start = 0

        for x in range(0, n):
            reserve = x - n + 1
            if reserve < 0:
                highest = max(self.cells[start:reserve])
            else:
                highest = max(self.cells[start:])
            value += highest * (10 ** (n - x - 1))
            start = self.cells.index(highest, start) + 1
        return value


if __name__ == "__main__":
    total_joltage = 0
    for line in fileinput.input(encoding="utf-8"):
        cells = [int(x) for x in list(line.strip())]
        bank = BatteryBank(cells)
        total_joltage += bank.max_joltage()
    print(total_joltage)
