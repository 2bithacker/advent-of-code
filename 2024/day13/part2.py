#!/usr/bin/env python3

import fileinput
import z3


class App(object):
    def __init__(self):
        self.buttons = {
            "A": None,
            "B": None,
        }
        self.prize = None
        self.spent = 0

    def button_mash(self) -> None:
        a = z3.Int("a")
        b = z3.Int("b")

        s = z3.Solver()
        s.add(
            (self.buttons["A"][0] * a) + (self.buttons["B"][0] * b)
            == (self.prize[0] + 10000000000000)
        )
        s.add(
            (self.buttons["A"][1] * a) + (self.buttons["B"][1] * b)
            == (self.prize[1] + 10000000000000)
        )

        if s.check() == z3.sat:
            m = s.model()
            a_presses = m.eval(a).as_long()
            b_presses = m.eval(b).as_long()

            cost = (3 * a_presses) + b_presses
            self.spent += cost
            print(
                f"Prize found: {self.prize} with {a_presses} A presses + {b_presses} B presses for a cost of {cost}"
            )

    def process_line(self, line: str) -> None:
        words = line.split(" ")
        match words[0]:
            case "Button":
                button = words[1][0]
                (_, x_offset) = words[2].strip(",").split("+")
                (_, y_offset) = words[3].split("+")
                self.buttons[button] = (int(x_offset), int(y_offset))
            case "Prize:":
                (_, x_loc) = words[1].strip(",").split("=")
                (_, y_loc) = words[2].split("=")
                self.prize = (int(x_loc), int(y_loc))
                self.button_mash()

    def __str__(self) -> str:
        return f"A: {self.buttons['A']}, B: {self.buttons['B']}, prize at {self.prize}."


if __name__ == "__main__":
    app = App()

    for line in fileinput.input(encoding="utf=8"):
        app.process_line(line.strip())

    print(app.spent)
