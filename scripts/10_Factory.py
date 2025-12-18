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
        button_list = self.buttons
        remaining_joltage = self.joltage.copy()
        # calculate number of presses for any button which appears only once in available presses
        all_buttons = [press for presses in self.buttons for press in presses]
        button_count = Counter(all_buttons)
        single_buttons = [button for button, num in button_count.items() if num == 1]
        tot_joltage = 0
        while single_buttons:
            for button in single_buttons:
                joltage = self.joltage[button]
                # which button press is this in? press this one joltage-1 times
                press = [p for p in self.buttons if button in p]
                button_list.remove(press[0])
                # what joltage does this give? remove from joltage
                for button in press[0]:
                    remaining_joltage[button] = remaining_joltage[button] - joltage
                tot_joltage += joltage
                if any(remaining_joltage) == 0:
                    single_buttons = False
                    break
            if single_buttons:
                remaining_buttons = [
                    press for presses in button_list for press in presses
                ]
                remaining_count = Counter(remaining_buttons)
                single_buttons = [
                    button for button, num in remaining_count.items() if num == 1
                ]
        print(remaining_joltage, tot_joltage)
        length = tot_joltage
        remaining_joltage, button_list, length = self.min_remaining_loop(
            remaining_joltage, button_list, length
        )
        return length

    def min_remaining_loop(self, remaining_joltage, button_list, length):
        min_remaining = min([x for x in remaining_joltage if x != 0])
        min_index = remaining_joltage.index(min_remaining)
        buttons_with_min = [press for press in button_list if min_index in press]
        if self.debug:
            print(
                f"{remaining_joltage=},{min_remaining=},{min_index=},{buttons_with_min=}"
            )
        for presses in combinations_with_replacement(buttons_with_min, min_remaining):
            total_presses = [light for lights in presses for light in lights]
            count = Counter(total_presses)
            new_joltage = [0] * self.size
            for p, num in count.items():
                new_joltage[p] = num
            leftover_joltage = [j - i for j, i in zip(remaining_joltage, new_joltage)]
            if self.debug:
                print(
                    f"{presses=}, {new_joltage=}, {remaining_joltage=}, {leftover_joltage=}"
                )
                if len(set(leftover_joltage)) == 1:
                    length += min_remaining
                    return leftover_joltage, button_list, length
                if any(x < 0 for x in leftover_joltage):
                    continue
                length += min_remaining
                unique_presses = {tuple(p) for p in presses}
                for press in unique_presses:
                    button_list.remove(list(press))
                remaining_joltage, button_list, length = self.min_remaining_loop(
                    leftover_joltage, button_list, length
                )
                return remaining_joltage, button_list, length
        return remaining_joltage, button_list, length

        # found = False
        # length = min_presses - 1
        # while not found:
        #         length += 1
        #         for presses in combinations_with_replacement(button_list, length):
        #             total_presses = [light for lights in presses for light in lights]
        #             count = Counter(total_presses)
        #             new_joltage = [0] * self.size
        #             for p, num in count.items():
        #                 new_joltage[p] = num
        #             if self.debug:
        #                 print(f"{presses=}, {new_joltage=}, {remaining_joltage=}")
        #             if new_joltage == remaining_joltage:
        #                 found = True
        #                 break
        return min_remaining + tot_joltage


# find smallest and set of buttons including it - find joltage after this?


test_machines = parse_data(test_data, debug=True)
test_machine_1 = test_machines[0]

# assert test_machine_1.button_press([1, 3]) == [".", "#", ".", "#"]

# assert test_machine_1.minimum_presses() == 2

test_machine_2 = test_machines[-1]

# assert test_machine_2.minimum_presses() == 2


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

# answer_1 = minimum_all_machines(input_data)
# print(answer_1)

# Part 2
print(test_machine_1.minimum_joltage_presses())
# assert test_machine_1.minimum_joltage_presses() == 10
print(test_machine_2.minimum_joltage_presses())
# assert test_machine_2.minimum_joltage_presses() == 11


def minimum_joltage_all_machines(data, debug=False):
    machines = parse_data(data)
    presses = 0
    for machine in machines:
        if debug:
            min_presses = machine.minimum_joltage_presses()
            print(f"{machine.indicator=},{min_presses=}")
        presses += machine.minimum_joltage_presses()
    return presses


# assert minimum_joltage_all_machines(test_data) == 33

# answer_2 = minimum_joltage_all_machines(input_data)
# print(answer_2)


# maybe we can build it up? Work out singles, then what's left of the other joltages
