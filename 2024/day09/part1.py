#!/usr/bin/env python3

import fileinput
import itertools
from rich.progress import track


class File(object):
    def __init__(self, fileno, size):
        self.id = fileno
        self.size = int(size)

    def __iter__(self):
        return itertools.repeat(self, self.size)

    def __repr__(self):
        return f"File({self.id}, {self.size})"


class App(object):
    def __init__(self):
        self.disk = list()

    def process_line(self, line):
        fileno = 0
        for x in range(0, len(line), 2):
            file = File(fileno, int(line[x]))
            self.disk.extend(file)

            fileno += 1
            try:
                self.disk.extend([None] * int(line[x + 1]))
            except IndexError:
                continue

    def checksum(self):
        return sum([x * self.disk[x].id for x in range(len(self.disk))])

    def run(self):
        for _ in track(self.disk, "Defragmenting..."):
            try:
                firstfree = self.disk.index(None)
            except ValueError:
                # no more free blocks
                break

            block = self.disk.pop()
            self.disk[firstfree] = block

        print(self.checksum())


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
