#!/usr/bin/env python3

import fileinput
from functools import cmp_to_key


class PageOrderException(Exception): ...


if __name__ == "__main__":
    rules = list()
    total = 0

    def page_check(x, y):
        if (x, y) in rules:
            return -1
        elif (y, x) in rules:
            return 1
        else:
            return 0

    for line in fileinput.input(encoding="utf=8"):
        if "|" in line:
            # rule line
            (x, y) = line.strip().split("|")
            rules.append((x, y))
            continue

        if "," in line:
            # page set
            pages = line.strip().split(",")
            try:
                for rule in rules:
                    try:
                        if pages.index(rule[0]) > pages.index(rule[1]):
                            raise PageOrderException()
                    except ValueError:
                        # rule page not in pages, ignore
                        pass
            except PageOrderException:
                pages.sort(key=cmp_to_key(page_check))
                total += int(pages[int(len(pages) / 2)])

    print(total)
