## Day 10: Factory

from itertools import combinations_with_replacement
from collections import Counter

# Part 1

test_data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def parse_data(data, debug=False):
    machines = []
    machine_list = data.split("\n")
    for machine in machine_list:
        first_split = machine.split("]")
        indicator = first_split[0][1:]
        second_split = first_split[1].split("{")
        buttons = second_split[0]
        joltage = second_split[1][:-1]
        machines.append(Machine(indicator, buttons, joltage, debug))
    return machines


class Machine:

    def __init__(self, indicator, buttons, joltage, debug=False):
        self.indicator = [x for x in indicator]
        self.indicator_list = self.make_indicator_list()
        self.buttons = self.parse_buttons(buttons)
        self.joltage = [int(jolt) for jolt in joltage.split(",")]
        self.size = len(self.indicator)
        self.current = ["."] * self.size
        self.debug = debug

    def __str__(self):
        return "".join(x for x in self.current)

    def parse_buttons(self, buttons):
        split_buttons = [press[1:-1] for press in buttons.split()]
        return [[int(x) for x in press.split(",")] for press in split_buttons]

    def make_indicator_list(self):
        indicator_list = []
        for num, light in enumerate(self.indicator):
            if light == "#":
                indicator_list.append(num)
        return indicator_list

    def button_press(self, press):
        for light in press:
            if self.current[light] == ".":
                self.current[light] = "#"
            elif self.current[light] == "#":
                self.current[light] = "."
        return self.current

    def minimum_presses(self):
        found = False
        for press in self.buttons:
            if set(press) == set(self.indicator_list):
                return 1
        length = 1
        while not found:
            length += 1
            for presses in combinations_with_replacement(self.buttons, length):
                total_presses = [light for lights in presses for light in lights]
                count = Counter(total_presses)
                odds = [light for light, num in count.items() if num % 2 != 0]
                if self.debug:
                    print(f"{presses=}, {odds=}, {self.indicator_list=}")
                # we need the number of presses on off lights to be even, and on lights to be odd
                # check if odd presses matches the indicator list
                if set(odds) == set(self.indicator_list):
                    found = True
                    break
        return length

    def minimum_joltage_presses(self):
        # need at least the maximum joltage number of presses
        min_presses = max(self.joltage)
        found = False
        if min_presses == 1:
            for press in self.buttons:
                new_joltage = [0] * self.size
                for p in press:
                    new_joltage[p] = 1
                if new_joltage == self.joltage:
                    return 1
        else:
            length = min_presses - 1
            while not found:
                length += 1
                for presses in combinations_with_replacement(self.buttons, length):
                    total_presses = [light for lights in presses for light in lights]
                    count = Counter(total_presses)
                    new_joltage = [0] * self.size
                    for p, num in count.items():
                        new_joltage[p] = num
                    if self.debug:
                        print(f"{presses=}, {new_joltage}=, {self.indicator_list=}")
                    # we need the number of presses on off lights to be even, and on lights to be odd
                    # check if odd presses matches the indicator list
                    if new_joltage == self.joltage:
                        found = True
                        break
        return length


test_machines = parse_data(test_data)
test_machine_1 = test_machines[0]

assert test_machine_1.button_press([1, 3]) == [".", "#", ".", "#"]

assert test_machine_1.minimum_presses() == 2

test_machine_2 = test_machines[-1]

assert test_machine_2.minimum_presses() == 2


def minimum_all_machines(data, debug=False):
    machines = parse_data(data)
    presses = 0
    for machine in machines:
        if debug:
            min_presses = machine.minimum_presses()
            print(f"{machine.indicator=},{min_presses=}")
        presses += machine.minimum_presses()
    return presses


assert minimum_all_machines(test_data) == 7

with open("../input_data/10_Factory.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_1 = minimum_all_machines(input_data)
print(answer_1)

# Part 2

assert test_machine_1.minimum_joltage_presses() == 10
assert test_machine_2.minimum_joltage_presses() == 11


def minimum_joltage_all_machines(data, debug=False):
    machines = parse_data(data)
    presses = 0
    for machine in machines:
        if debug:
            min_presses = machine.minimum_joltage_presses()
            print(f"{machine.indicator=},{min_presses=}")
        presses += machine.minimum_joltage_presses()
    return presses


assert minimum_joltage_all_machines(test_data) == 33

answer_2 = minimum_joltage_all_machines(input_data)
print(answer_2)
