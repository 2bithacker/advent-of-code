#!/usr/bin/env python3

import fileinput
from rich.progress import track


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

    def clear_visited(self):
        for row in self.grid:
            for tile in row:
                tile.visited = False

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
        self.starting_pos = None
        self.starting_dir = None
        self.loop_count = 0

    def process_line(self, line):
        row = self.map.add_row()

        for char in line:
            tile = Tile(char)
            row.append(tile)
            if char == "^":
                self.cursor = Cursor(len(self.map.grid) - 1, len(row) - 1)
                self.starting_pos = self.cursor.position
                self.starting_dir = self.cursor.direction

    def test_grid(self):
        self.cursor = Cursor(self.starting_pos[0], self.starting_pos[1])
        self.map.clear_visited()
        record = set()
        try:
            while True:
                record.add((self.cursor.position, self.cursor.direction))
                next_tile = self.map.get_tile(self.cursor.next_position())
                if next_tile.blocked:
                    self.cursor.turn()
                else:
                    self.cursor.move()
                    next_tile.visited = True

                if (self.cursor.position, self.cursor.direction) in record:
                    # loop detected
                    self.loop_count += 1
                    return record
        except OffMapException:
            # no loop detected, went off the grid
            pass

        return record

    def run(self):
        # run once with no obsctruction to get normal path
        path = set([x[0] for x in self.test_grid()])
        for step in track(path, "Reticulating splines..."):
            # for each step in the normal path, try an obstruction there
            if step == self.starting_pos:
                continue
            tile = self.map.get_tile(step)
            tile.blocked = True
            self.test_grid()
            tile.blocked = False

        print(self.loop_count)


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
