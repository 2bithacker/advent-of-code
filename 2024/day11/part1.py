#!/usr/bin/env python3

import fileinput


class Stone(object):
    def __init__(self, number: int):
        self.number = number

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self) -> str:
        return f"Stone({self.number})"

    def blink(self) -> list:
        if self.number == 0:
            self.number = 1
            return [self]

        if len(str(self.number)) % 2 == 0:
            string = str(self.number)
            halflen = int(len(string) / 2)
            self.number = int(string[:halflen])
            new_stone = Stone(int(string[halflen:]))
            return [self, new_stone]

        self.number *= 2024
        return [self]


class App(object):
    def __init__(self):
        self.line = list()

    def process_line(self, line: str):
        for number in line.split(" "):
            stone = Stone(int(number))
            self.line.append(stone)

    def run(self):
        for _ in range(25):
            new_line = list()
            for stone in self.line:
                new_line.extend(stone.blink())
            self.line = new_line

        print(len(self.line))


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
