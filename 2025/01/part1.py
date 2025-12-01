#!/usr/bin/env python3

import fileinput


class Dial(object):
    def __init__(self):
        self.position = 50
        self.zero_count = 0

    def left(self, clicks):
        self.position -= clicks
        while self.position < 0:
            self.position = 100 + self.position
        if self.position == 0:
            self.zero_count += 1

    def right(self, clicks):
        self.position += clicks
        while self.position > 99:
            self.position -= 100
        if self.position == 0:
            self.zero_count += 1


if __name__ == "__main__":
    dial = Dial()
    for line in fileinput.input(encoding="utf-8"):
        direction = line[0]
        clicks = int(line[1:])
        print(f"Position: {dial.position} {direction} {clicks}")
        match direction:
            case "L":
                dial.left(clicks)
            case "R":
                dial.right(clicks)

    print(dial.zero_count)
