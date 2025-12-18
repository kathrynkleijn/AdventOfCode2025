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
        self.equations = []
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

    def joltage_equation_system(self):
        for button in range(self.size):
            equation = [0] * len(self.buttons)
            for num, press in enumerate(self.buttons):
                if button in press:
                    equation[num] = 1
            equation.append(self.joltage[button])
            self.equations.append(equation)
        return self.equations

    def sort_equations(self):
        self.equations = sorted(self.equations)[::-1]
        return self.equations

    def row_echelon(self):
        m = len(self.equations)
        for j in range(1, m):
            for i in range(j, m):
                if self.equations[i][j - 1] != 0:
                    multiplier = self.equations[i][j - 1] / self.equations[j - 1][j - 1]
                    self.equations[i] = [
                        y - multiplier * x
                        for x, y in zip(self.equations[j - 1], self.equations[i])
                    ]
        return self.equations

    def reduced_row_echelon(self):
        m = len(self.equations)
        n = len(self.equations[0])
        for j in reversed(range(m - 1)):
            for i in range(j + 1, n - 1):
                if (
                    self.equations[j + 1][i] == self.equations[j][i]
                    and self.equations[j][i] != 0
                ):
                    self.equations[j] = [
                        int(x - y)
                        for x, y in zip(self.equations[j], self.equations[j + 1])
                    ]
                    break
        return self.equations

    def find_free_variables(self):
        free = []
        n = len(self.equations[0])
        for j in range(n - 1):
            col = [x[j] for x in self.equations]
            print(col)
            if Counter(col)[1] > 1:
                free.append(j)
        return free

    def find_solutions(self, free):
        for i in range():
            for j in range():
                partial_solution = [None] * len(self.equations[0])
                partial_solution[free[0]] = i
                partial_solution[free[1]] = j
                for equation in self.equations[::-1]:
                    # need to keep sign of x
                    equation_solution = [
                        partial_solution[num] if x != 0 else x
                        for num, x in enumerate(equation[:-1])
                    ]
                    solution = equation[-1] - sum(equation_solution)
                    # check if equation solution makes sense
                    if solution >= 0:
                        partial_solution


test_machines = parse_data(test_data, debug=True)
test_machine_1 = test_machines[0]

# assert test_machine_1.button_press([1, 3]) == [".", "#", ".", "#"]

# assert test_machine_1.minimum_presses() == 2

# test_machine_2 = test_machines[-1]

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


assert test_machine_1.joltage_equation_system() == [
    [0, 0, 0, 0, 1, 1, 3],
    [0, 1, 0, 0, 0, 1, 5],
    [0, 0, 1, 1, 1, 0, 4],
    [1, 1, 0, 1, 0, 0, 7],
]
assert test_machine_1.sort_equations() == [
    [1, 1, 0, 1, 0, 0, 7],
    [0, 1, 0, 0, 0, 1, 5],
    [0, 0, 1, 1, 1, 0, 4],
    [0, 0, 0, 0, 1, 1, 3],
]

print(test_machine_1.reduced_row_echelon())
print(test_machine_1.find_free_variables())
# assert test_machine_1.minimum_joltage_presses() == 10
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
