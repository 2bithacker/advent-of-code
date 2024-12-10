#!/usr/bin/env python3

import fileinput


class Node(object):
    def __init__(self, location: tuple, elevation: int):
        self.location = location
        self.elevation = elevation

    def __str__(self) -> str:
        return str(self.elevation)

    def __repr__(self) -> str:
        return f"Node({self.location}, {self.elevation})"

    def is_trailhead(self) -> bool:
        return self.elevation == 0

    def __getitem__(self, item):
        return self.location[item]


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

    def neighbors(self, location) -> list:
        results = list()
        for x, y in ((-1, 0), (0, 1), (0, -1), (1, 0)):
            coords = (location[0] + x, location[1] + y)
            try:
                results.append(self[coords])
            except IndexError:
                continue
        return results

    def add_line(self) -> int:
        self.map.append(list())
        return len(self.map) - 1

    def print(self):
        for line in self.map:
            print("".join([str(x) for x in line]))


class App(object):
    def __init__(self):
        self.map = Grid()
        self.trailheads = list()
        self.peaks = dict()

    def process_line(self, line: str):
        x = self.map.add_line()
        for y in range(len(line)):
            new_node = Node((x, y), int(line[y]))
            self.map[x].append(new_node)

            if new_node.is_trailhead():
                self.trailheads.append(new_node)

    def trace_path(self, head: Node, here: Node):
        for node in self.map.neighbors(here):
            if node.elevation - here.elevation == 1:
                if node.elevation == 9:
                    # peak found, score!
                    self.peaks[head].add(node)
                else:
                    # path continues
                    self.trace_path(head, node)

    def run(self):
        for trailhead in self.trailheads:
            self.peaks[trailhead] = set()
            self.trace_path(trailhead, trailhead)
            print(f"Score of {trailhead.location}: {len(self.peaks[trailhead])}")

        print(sum([len(self.peaks[x]) for x in self.peaks]))


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
