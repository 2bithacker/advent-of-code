#!/usr/bin/env python3

import fileinput
import math
import functools


def digits(number: int) -> int:
    if number <= 999999999999997:
        return int(math.log10(number)) + 1
    else:
        return len(str(number))


@functools.cache
def process_stone(number: int) -> tuple:
    if number == 0:
        return (1,)

    intlen = digits(number)
    if intlen % 2 == 0:
        left_number = int(number / (10 ** (intlen / 2)))
        right_number = int(number - (left_number * (10 ** (intlen / 2))))
        return (left_number, right_number)

    return (number * 2024,)


@functools.cache
def blink(stones: tuple[int, ...], n: int) -> int:
    if n == 0:
        return len(stones)

    return sum(blink(process_stone(stone), n - 1) for stone in stones)


if __name__ == "__main__":
    for line in fileinput.input(encoding="utf=8"):
        stones = tuple(map(int, line.strip().split(" ")))
        result = blink(stones, 75)
        print(result)
