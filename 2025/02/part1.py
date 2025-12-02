#!/usr/bin/env python3

import fileinput


class ProductRange(object):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def find_invalid(self) -> int:
        tally = 0
        for product_id in range(self.start, self.end + 1):
            str_pid = str(product_id)
            str_len = len(str_pid)
            if str_len % 2 == 1:
                # odd length, skip it
                continue
            if str_pid[: str_len // 2] == str_pid[str_len // 2 :]:
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
