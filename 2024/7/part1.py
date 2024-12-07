#!/usr/bin/env python3

import fileinput
from operator import add, mul


class App(object):
    def __init__(self):
        self.total = 0
        self.target = None

    def operate(self, numerals):
        left = numerals.pop(0)
        right = numerals.pop(0)
        for func in (add, mul):
            result = func(left, right)
            if result > self.target:
                # don't bother recursing if we're over target, nothing makes it smaller
                continue
            if numerals:
                ncopy = numerals.copy()
                ncopy.insert(0, result)
                result = self.operate(ncopy)
            if result == self.target:
                return result

    def process_line(self, line):
        (target, numeral_string) = line.split(": ")
        numerals = [int(x) for x in numeral_string.split(" ")]
        self.target = int(target)

        result = self.operate(numerals)
        if result == self.target:
            self.total += result


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    print(app.total)
