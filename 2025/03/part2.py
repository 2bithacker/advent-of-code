#!/usr/bin/env python3

import fileinput


class BatteryBank(object):
    def __init__(self, cells: list):
        self.cells = cells

    def max_joltage(self, n=12) -> int:
        value = 0
        available_cells = self.cells.copy()

        for x in range(0, n):
            reserve = x - n + 1
            if reserve < 0:
                highest = max(available_cells[:reserve])
            else:
                highest = max(available_cells)
            value += highest * (10 ** (n - x - 1))
            h_index = available_cells.index(highest) + 1
            available_cells = available_cells[h_index:]
        return value


if __name__ == "__main__":
    total_joltage = 0
    for line in fileinput.input(encoding="utf-8"):
        cells = [int(x) for x in list(line.strip())]
        bank = BatteryBank(cells)
        total_joltage += bank.max_joltage()
    print(total_joltage)
