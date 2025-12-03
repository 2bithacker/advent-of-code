#!/usr/bin/env python3

import fileinput


class BatteryBank(object):
    def __init__(self, cells: list):
        self.cells = cells

    def max_joltage(self) -> int:
        first = max(self.cells[:-1])
        first_index = self.cells.index(first)
        second = max(self.cells[first_index + 1 :])
        return (first * 10) + second


if __name__ == "__main__":
    total_joltage = 0
    for line in fileinput.input(encoding="utf-8"):
        cells = [int(x) for x in list(line.strip())]
        bank = BatteryBank(cells)
        total_joltage += bank.max_joltage()
    print(total_joltage)
