#!/usr/bin/env python3

import fileinput


class PageOrderException(Exception): ...


if __name__ == "__main__":
    rules = list()
    total = 0

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
                total += int(pages[int(len(pages) / 2)])
            except PageOrderException:
                pass

    print(total)
