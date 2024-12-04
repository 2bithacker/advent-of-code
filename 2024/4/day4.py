#!/usr/bin/env python3

import fileinput

DIRECTIONS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))


class WordGrid(object):
    def __init__(self, target):
        self.matrix = list()
        self.target = target
        self.total = 0

    def search(self):
        for x in range(0, len(self.matrix)):
            for y in range(0, len(self.matrix[x])):
                if self.matrix[x][y] == self.target[0]:
                    for direction in DIRECTIONS:
                        if self.check_direction(x, y, direction, 1):
                            self.total += 1

    def check_direction(self, x, y, direction, offset):
        my_x = x + direction[0]
        my_y = y + direction[1]

        if my_x < 0 or my_y < 0:
            return False

        try:
            if self.matrix[my_x][my_y] == self.target[offset]:
                if offset + 1 < len(self.target):
                    return self.check_direction(my_x, my_y, direction, offset + 1)
                else:
                    return True
            else:
                return False
        except IndexError:
            return False


if __name__ == "__main__":
    grid = WordGrid("XMAS")

    for line in fileinput.input(encoding="utf=8"):
        row = line.strip()
        grid.matrix.append(row)

    grid.search()

    print(grid.total)
