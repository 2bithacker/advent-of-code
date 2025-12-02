#!/usr/bin/env python3

import fileinput
import re


class ProductRange(object):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.pattern = re.compile(r"^(\d+)\1+$")

    def find_invalid(self) -> int:
        tally = 0
        for product_id in range(self.start, self.end + 1):
            if self.pattern.match(str(product_id)):
                tally += product_id
                print(f"{self.start}-{self.end}: invalid ID {product_id}")

        return tally


if __name__ == "__main__":
    for line in fileinput.input(encoding="utf-8"):
        total = 0
        for product_range in line.split(","):
            (start, end) = product_range.split("-")
            pr = ProductRange(int(start), int(end))
            total += pr.find_invalid()
        print(total)
