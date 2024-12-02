#!/usr/bin/env python3

import fileinput

class LevelException(Exception):
    pass

def test_level_pair(increasing, x, y):
    # increasing, but next number is lower
    if increasing and x > y:
        raise LevelException(f"increasing but {x} > {y}")

    # decreasing, but next number is higher
    if not increasing and x < y:
        raise LevelException(f"decreasing but {x} < {y}")

    # difference <1 or >3
    if not(0 < abs(x - y) < 4):
        raise LevelException(f"level change {x} .. {y} is not between 1 and 3")

def test_levels(levels, recurse=False):
    print(f"{' '.join(map(str,levels))}")
    increasing = None

    for x in range(0, len(levels)-1):
        if increasing == None:
            if levels[x] < levels[x+1]:
                increasing = True
            elif levels[x] > levels[x+1]:
                increasing = False

        # First try on full set, if it passes, we're good.
        try:
            test_level_pair(increasing, levels[x], levels[x+1])
        except LevelException as e:
            print(f"Error on position {x}: {e}")
            if not recurse:
                raise

            # Try again with x-1, x, x+1 removed, if any of these pass, we're good
            for y in range(x-1, x+2):
                if y < 0:
                    continue
                try:
                    l = levels.copy()
                    del l[y]
                    test_levels(l)
                    return
                except LevelException as le:
                    print(f"Error on position {x}: {le}")

            raise

if __name__ == "__main__":
    safe_count = 0

    for line in fileinput.input(encoding="utf=8"):
        levels = [int(x) for x in line.split()]
        try:
            test_levels(levels, True)
            safe_count += 1
            print("Safe")
        except LevelException as e:
            print("Unsafe")
            pass

    print(safe_count)
