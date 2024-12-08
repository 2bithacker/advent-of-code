#!/usr/bin/env python3

import fileinput
import itertools
from collections import defaultdict


class Node(object):
    def __init__(self, location):
        self.location = location
        self.antenna = None
        self.antinode = False

    def __str__(self):
        if self.antenna:
            return self.antenna
        if self.antinode:
            return "#"
        return "."

    def __repr__(self):
        return f"Node({self.location}, {self.antenna})"

    def __add__(self, other):
        if hasattr(other, "location"):
            x = self.location[0] + other.location[0]
            y = self.location[1] + other.location[1]
        else:
            x = self.location[0] + other[0]
            y = self.location[1] + other[1]
        return (x, y)

    def __sub__(self, other):
        if hasattr(other, "location"):
            x = self.location[0] - other.location[0]
            y = self.location[1] - other.location[1]
        else:
            x = self.location[0] - other[0]
            y = self.location[1] - other[1]
        return (x, y)

    def __gt__(self, other):
        return sum(self.location) > sum(other.location)


class Grid(object):
    def __init__(self):
        self.map = list()

    def __getitem__(self, item):
        try:
            if item[0] < 0 or item[1] < 0:
                raise IndexError("coordinates off of map")
            return self.map[item[0]][item[1]]
        except TypeError:
            return self.map[item]

    def add_line(self):
        self.map.append(list())
        return len(self.map) - 1

    def print(self):
        for line in self.map:
            print("".join([str(x) for x in line]))


class App(object):
    def __init__(self):
        self.map = Grid()
        self.frequencies = defaultdict(list)
        self.antinodes = 0

    def process_line(self, line):
        x = self.map.add_line()
        for y in range(len(line)):
            new_node = Node((x, y))
            self.map[x].append(new_node)
            if line[y] != ".":
                new_node.antenna = line[y]
                self.frequencies[line[y]].append(new_node)

    def set_antinode(self, loc):
        if not self.map[loc].antinode:
            self.map[loc].antinode = True
            self.antinodes += 1

    def run(self):
        for frequency in self.frequencies:
            for pair in itertools.combinations(self.frequencies[frequency], 2):
                diff = pair[0] - pair[1]
                antinodes = list()
                antinodes.append(pair[0] + diff)
                antinodes.append(pair[1] - diff)

                for loc in antinodes:
                    try:
                        if not self.map[loc].antinode:
                            self.map[loc].antinode = True
                            self.antinodes += 1
                    except IndexError:
                        continue

        self.map.print()
        print(self.antinodes)


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
