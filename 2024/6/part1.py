#!/usr/bin/env python3

import fileinput


class OffMapException(Exception): ...


class Tile(object):
    def __init__(self, contents):
        self.visited = False
        self.blocked = False

        if contents == "^":
            self.visited = True
        elif contents == "#":
            self.blocked = True

    def __str__(self) -> str:
        if self.blocked:
            return "#"
        if self.visited:
            return "X"
        return "."

    def __repr__(self) -> str:
        return str(self)


class Map(object):
    def __init__(self):
        self.grid = list()

    def add_row(self):
        row = list()
        self.grid.append(row)
        return row

    def get_tile(self, pos) -> Tile:
        if pos[0] < 0 or pos[1] < 0:
            raise OffMapException()
        try:
            return self.grid[pos[0]][pos[1]]
        except IndexError:
            raise OffMapException()

    def total_visited(self) -> int:
        total = 0
        for row in self.grid:
            for tile in row:
                if tile.visited:
                    total += 1
        return total

    def print(self):
        for row in self.grid:
            print("".join([str(x) for x in row]))


class Cursor(object):
    DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))

    def __init__(self, x, y):
        self.direction = Cursor.DIRECTIONS[0]
        self.position = (x, y)

    def print(self):
        print(f"Cursor at {self.position} facing {self.direction}")

    def next_position(self):
        return (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        )

    def move(self):
        (x, y) = self.next_position()
        if x >= 0 and y >= 0:
            self.position = (x, y)
        else:
            raise OffMapException()

    def turn(self):
        cur_direction = Cursor.DIRECTIONS.index(self.direction) + 1
        new_direction = cur_direction % len(Cursor.DIRECTIONS)
        self.direction = Cursor.DIRECTIONS[new_direction]


class App(object):
    def __init__(self):
        self.map = Map()
        self.start = None
        self.cursor = None

    def process_line(self, line):
        row = self.map.add_row()

        for char in line:
            tile = Tile(char)
            row.append(tile)
            if char == "^":
                self.cursor = Cursor(len(self.map.grid) - 1, len(row) - 1)

    def run(self):
        try:
            while True:
                next_tile = self.map.get_tile(self.cursor.next_position())
                if next_tile.blocked:
                    self.cursor.turn()
                else:
                    self.cursor.move()
                    next_tile.visited = True
        except OffMapException:
            self.map.print()
            print(self.map.total_visited())


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
