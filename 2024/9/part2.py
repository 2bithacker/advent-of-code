#!/usr/bin/env python3

import fileinput
import itertools
from rich.progress import (
    Progress,
    MofNCompleteColumn,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)


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
        self.files = dict()

    def process_line(self, line):
        fileno = 0
        for x in range(0, len(line), 2):
            file = File(fileno, int(line[x]))
            self.disk.extend(file)
            self.files[fileno] = file

            fileno += 1
            try:
                self.disk.extend([None] * int(line[x + 1]))
            except IndexError:
                continue

    def __repr__(self):
        string = ""
        for block in self.disk:
            if block is None:
                string += "."
            else:
                string += str(block.id % 10)
        return string

    def checksum(self):
        return sum(
            [
                x * self.disk[x].id
                for x in range(len(self.disk))
                if self.disk[x] is not None
            ]
        )

    def find_free_blocks(self):
        blockmap = list()
        for x in range(len(self.disk)):
            blockmap.append((self.disk[x], x))

        freeblocks = list()
        for k, g in itertools.groupby(blockmap, lambda x: x[0]):
            if k is None:
                block = list(g)
                size = len(block)
                start = block[0][1]
                freeblocks.append((start, size))
        return freeblocks

    def move_file(self, id, loc):
        file = self.files[id]
        while file in self.disk:
            self.disk[self.disk.index(file)] = None

        for x in range(0, file.size):
            self.disk[loc + x] = file

    def run(self):
        file_ids = sorted(self.files.keys(), reverse=True)

        freeblocks = self.find_free_blocks()

        progress = Progress(
            TextColumn("[progress.description]Defragmenting..."),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            MofNCompleteColumn(),
            SpinnerColumn(),
        )

        with progress:
            for id in progress.track(file_ids):
                start = self.disk.index(self.files[id])
                for block in freeblocks:
                    if block[0] >= start:
                        # don't consider free space after the start of this file
                        break
                    if block[1] >= self.files[id].size:
                        self.move_file(id, block[0])
                        freeblocks = self.find_free_blocks()
                        break

        print(self.checksum())


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
