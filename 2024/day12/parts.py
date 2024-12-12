#!/usr/bin/env python3

import fileinput

#             RIGHT   DOWN    LEFT     UP
HEADING = ((0, 1), (1, 0), (0, -1), (-1, 0))
DIAGONALS = ((1, 1), (-1, 1), (1, -1), (-1, -1))


class Plot(object):
    def __init__(self, location: tuple, plants: str):
        self.location = location
        self.plants = plants
        self.region = None

    def __str__(self) -> str:
        return str(self.plants)

    def __repr__(self) -> str:
        return f"Plot({self.location}, {self.plants})"

    def __getitem__(self, item):
        return self.location[item]


class Region(object):
    def __init__(self, plants: str):
        self.area = 0
        self.perimeter = 0
        self.plants = plants
        self.plots = set()
        self.edges = 0

    def fencing_a(self) -> int:
        return self.area * self.perimeter

    def fencing_b(self) -> int:
        return self.area * self.edges

    def __str__(self):
        return f"region of {self.plants} plants with A: {self.area} * {self.perimeter} = {self.fencing_a()}. B: {self.area} * {self.edges} = {self.fencing_b()}"

    def print(self):
        locations = [p.location for p in self.plots]
        loc_map = {p.location: p for p in self.plots}
        for r in range(max([p[0] for p in locations]) + 1):
            line = ""
            for c in range(max([p[1] for p in locations]) + 1):
                if (r, c) in locations:
                    line += str(loc_map[(r, c)])
                else:
                    line += "."
            print(line)

    def double_map(self) -> list:
        lines = list()

        locations = [p.location for p in self.plots]

        non_empty = False
        for r in range(max([p[0] for p in locations]) + 1):
            line = str()
            for c in range(max([p[1] for p in locations]) + 1):
                if (r, c) in locations:
                    line += "XX"
                else:
                    line += ".."
            if "X" in line:
                non_empty = True
            if non_empty:
                lines.append(line)
                lines.append(line)

        return lines


class Map(object):
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
                results.append(None)
        return results

    def diag_neighbors(self, location) -> list:
        results = list()
        for x, y in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            coords = (location[0] + x, location[1] + y)
            try:
                results.append(self[coords])
            except IndexError:
                results.append(None)
        return results

    def get_neighbor(self, loc: tuple[int, int], dir: tuple[int, int]) -> Plot:
        (x, y) = (loc[0] + dir[0], loc[1] + dir[1])
        try:
            return self[x][y]
        except IndexError:
            return None

    def add_line(self) -> int:
        self.map.append(list())
        return len(self.map) - 1

    def print(self):
        for line in self.map:
            print("".join([str(x) for x in line]))


class App(object):
    def __init__(self):
        self.map = Map()
        self.regions = set()

    def process_line(self, line: str) -> None:
        x = self.map.add_line()
        for y in range(len(line)):
            new_node = Plot((x, y), line[y])
            self.map[x].append(new_node)

    def check_plot(self, plot: Plot) -> None:
        if not plot.region:
            region = Region(plot.plants)
            plot.region = region
            region.plots.add(plot)
            self.regions.add(plot.region)
            plot.region.area += 1
        else:
            region = plot.region

        perimeter = 4

        # First, examine all connected neighbors to set region correctly
        for neighbor in self.map.neighbors(plot):
            if neighbor and neighbor.plants == plot.plants:
                perimeter -= 1
                if not neighbor.region:
                    neighbor.region = plot.region
                    region.plots.add(neighbor)
                    plot.region.area += 1
                    self.check_plot(neighbor)

        plot.region.perimeter += perimeter

    def check_edges(self, region: Region) -> None:
        bigmap = region.double_map()
        corners = 0

        for c in range(len(bigmap)):
            for r in range(len(bigmap[c])):
                if bigmap[c][r] == ".":
                    continue
                if bigmap[c][r] == "X":
                    others = 0
                    for d in HEADING:
                        (cd, rd) = (c + d[0], r + d[1])
                        try:
                            if cd < 0 or rd < 0:
                                others += 1
                            elif bigmap[cd][rd] == ".":
                                others += 1
                        except IndexError:
                            others += 1
                    if others == 0:
                        # could be inside corner, check diagonally
                        for d in DIAGONALS:
                            (cd, rd) = (c + d[0], r + d[1])
                            if bigmap[cd][rd] == ".":
                                # yup, it's an inside corner
                                corners += 1
                                break
                    elif others == 2:
                        # outside corner
                        corners += 1

        region.edges = corners

    def run(self) -> None:
        self.map.print()

        for line in self.map.map:
            for plot in line:
                if not plot.region:
                    self.check_plot(plot)

        for region in self.regions:
            self.check_edges(region)
            print(f"A {region}")

        print("Part 1:", sum([region.fencing_a() for region in self.regions]))
        print("Part 2:", sum([region.fencing_b() for region in self.regions]))


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    app.run()
