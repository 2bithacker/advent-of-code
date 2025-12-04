#!/usr/bin/env python3

import fileinput

DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


class Cell(object):
    def __init__(self, grid, position, value):
        self.grid = grid
        self.position = position
        self.value = value

    def accessible(self) -> bool:
        if self.value != "@":
            return False

        full = 0
        empty = 0
        for cell in self.grid.neighbors(self.position):
            if cell:
                match cell.value:
                    case ".":
                        empty += 1
                    case "@":
                        full += 1
                    case "X":
                        full += 1
            else:
                empty += 1

            if full > 3:
                return False
            if empty > 4:
                self.value = "X"
                return True

        self.value = "X"
        return True

    def __str__(self):
        return f"[{self.value}] @ {self.position}"

    def __repr__(self):
        return f"[{self.value}] @ {self.position}"


class Grid(object):
    def __init__(self):
        self.grid = list()

    def add_row(self, row_data: list) -> None:
        y = len(self.grid)
        row = list()
        self.grid.append(row)
        for x in range(0, len(row_data)):
            c = Cell(self, (y, x), row_data[x])
            row.append(c)

    def print(self) -> None:
        for row in self.grid:
            print("".join([c.value for c in row]))

    def check_access(self) -> int:
        accessible = 0
        for cell in [c for row in self.grid for c in row]:
            if cell.accessible():
                accessible += 1
        return accessible

    def remove_accessible(self) -> None:
        for cell in [c for row in self.grid for c in row]:
            if cell.value == "X":
                cell.value = "."

    def check_and_remove(self) -> int:
        removed = 0
        while True:
            accessible = self.check_access()
            if accessible > 0:
                removed += accessible
                self.remove_accessible()
            else:
                break
        return removed

    def neighbors(self, pos) -> list:
        neighbors = list()
        for offset in DIRECTIONS:
            n_pos = (pos[0] + offset[0], pos[1] + offset[1])
            if (n_pos[0] < 0) or (n_pos[1] < 0):
                neighbors.append(None)
                continue

            try:
                neighbors.append(self.grid[n_pos[0]][n_pos[1]])
            except IndexError:
                neighbors.append(None)
        return neighbors


if __name__ == "__main__":
    grid = Grid()
    for line in fileinput.input(encoding="utf-8"):
        cells = list(line.strip())
        grid.add_row(cells)
    print(grid.check_and_remove())
