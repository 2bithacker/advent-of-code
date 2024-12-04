#!/usr/bin/env python3

import fileinput

CROSSES = ((-1, -1), (-1, 1), (1, 1), (1, -1))


class WordGrid(object):
    def __init__(self):
        self.matrix = list()
        self.total = 0

    def offset(self, x, y, os):
        my_x = x + os[0]
        my_y = y + os[1]
        return self.matrix[my_x][my_y]

    def search(self):
        for x in range(1, len(self.matrix) - 1):
            for y in range(1, len(self.matrix[x]) - 1):
                if self.matrix[x][y] == "A":
                    if self.check_position(x, y):
                        self.total += 1

    def check_position(self, x, y):
        for start in (0, 1):
            opposite = (start + 2) % len(CROSSES)
            if (
                self.offset(x, y, CROSSES[start]) == "M"
                and self.offset(x, y, CROSSES[opposite]) == "S"
            ):
                continue
            elif (
                self.offset(x, y, CROSSES[start]) == "S"
                and self.offset(x, y, CROSSES[opposite]) == "M"
            ):
                continue
            else:
                return False
        return True


if __name__ == "__main__":
    grid = WordGrid()

    for line in fileinput.input(encoding="utf=8"):
        row = line.strip()
        grid.matrix.append(row)

    grid.search()

    print(grid.total)
