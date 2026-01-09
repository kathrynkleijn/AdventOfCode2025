## Day 10: Factory

from itertools import combinations_with_replacement, product, groupby
from collections import Counter
import math

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
        self.sort_equations()
        self.equations = list(k for k, _ in groupby(self.equations))
        return self.equations

    def sort_equations(self):
        self.equations = sorted(self.equations)[::-1]
        return self.equations

    def reset_equations(self):
        self.equations = []

    def row_echelon(self):
        m = len(self.equations)
        for j in range(1, m):
            # not all([val == 0 for val in self.equations[j]]) and
            if not all([val == 0 for val in self.equations[j - 1]]):
                # n = next(
                #     index for index, val in enumerate(self.equations[j]) if val != 0
                # )
                p = next(
                    index for index, val in enumerate(self.equations[j - 1]) if val != 0
                )
                if p > j - 1:
                    self.make_positive()
                    self.sort_equations()
                    # print("sorted")
            for i in range(j, m):
                # print(f"{j=}")
                if self.equations[i][j - 1] != 0 and self.equations[j - 1][j - 1] != 0:
                    # print("\n")
                    # print(self.equations[i], self.equations[j - 1])
                    multiplier = self.equations[i][j - 1] / self.equations[j - 1][j - 1]
                    if multiplier % 1 != 0:
                        if abs(multiplier) < 0:
                            multiplier = 1 / multiplier
                            self.equations[i] = [
                                multiplier * y - x
                                for x, y in zip(
                                    self.equations[j - 1], self.equations[i]
                                )
                            ]
                        else:
                            hcf = math.gcd(
                                int(self.equations[i][j - 1]),
                                int(self.equations[j - 1][j - 1]),
                            )
                            multi_x = self.equations[i][j - 1] / hcf
                            multi_y = self.equations[j - 1][j - 1] / hcf
                            self.equations[i] = [
                                multi_y * y - multi_x * x
                                for x, y in zip(
                                    self.equations[j - 1], self.equations[i]
                                )
                            ]
                    else:
                        self.equations[i] = [
                            y - multiplier * x
                            for x, y in zip(self.equations[j - 1], self.equations[i])
                        ]
                    # if any([val % 1 != 0 for val in self.equations[i]]):

                    #     self.equations[i] = [
                    #         val / multiplier for val in self.equations[i]
                    #     ]
                    # print(f"{i=},{j=}")
                    # print("\n".join(str(equation) for equation in self.equations))
        self.make_positive()
        # print("\n")
        # print("\n".join(str(equation) for equation in self.sort_equations()))
        return self.sort_equations()

    def reduced_row_echelon(self):
        self.equations = [
            equation for equation in self.equations if equation != [0] * len(equation)
        ]
        self.equations = list(k for k, _ in groupby(self.equations))
        m = len(self.equations)
        n = next(index for index, val in enumerate(self.equations[-1]) if val != 0)
        for j in reversed(range(m)):
            for k in range(j):
                update = False
                for i in range(j, n + 1):
                    if self.equations[j - k - 1][i] != 0 and self.equations[j][i] != 0:
                        update = True
                        multiplier = self.equations[j - k - 1][i] / self.equations[j][i]
                        if multiplier % 1 != 0:
                            if abs(multiplier) < 0:
                                multiplier = 1 / multiplier
                                self.equations[j - k - 1] = [
                                    y - multiplier * x
                                    for x, y in zip(
                                        self.equations[j - k - 1], self.equations[j]
                                    )
                                ]
                            else:
                                hcf = math.gcd(
                                    int(self.equations[j - k - 1][i]),
                                    int(self.equations[j][i]),
                                )
                                multi_x = self.equations[j][i] / hcf
                                multi_y = self.equations[j - k - 1][i] / hcf
                                self.equations[j - k - 1] = [
                                    multi_y * y - multi_x * x
                                    for x, y in zip(
                                        self.equations[j - k - 1], self.equations[j]
                                    )
                                ]
                        else:
                            self.equations[j - k - 1] = [
                                multiplier * y - x
                                for x, y in zip(
                                    self.equations[j - k - 1], self.equations[j]
                                )
                            ]
                        # print("\n")
                        # print("\n".join(str(equation) for equation in self.equations))
                        if update:
                            break
            self.make_positive()
        self.equations = [
            equation for equation in self.equations if equation != [0] * len(equation)
        ]
        self.make_positive()
        return self.sort_equations()

    def make_positive(self):
        for num, equation in enumerate(self.equations):
            self.equations[num] = [int(val) for val in equation]
            if any([val < 0 for val in equation]):
                if next(val for val in equation if val) < 0:
                    self.equations[num] = [int(val) * -1 for val in equation]

    def find_free_variables(self):
        m = len(self.equations)
        n = len(self.equations[0])
        num_free = (n - 1) - m
        free = []
        diagonals = []
        for equation in self.equations:
            diagonal = next(index for index, val in enumerate(equation) if val != 0)
            diagonals.append(diagonal)
        for j in range(n - 1):
            if j not in diagonals:
                free.append(j)
        if len(free) != num_free:
            print("help!")
        return free

    def range_for_free(self, free):
        ranges = {}
        for equation in self.equations[::-1]:
            unknowns = [(num, val) for num, val in enumerate(equation[:-1]) if val != 0]
            # check if equation has only two variables
            num_variables = len(unknowns)
            # check that one of them is a free variable
            free_variables = [num for num, _ in unknowns if num in free]
            if num_variables == 1 and free_variables:
                free.remove(free_variables[0])
            if num_variables == 2 and free_variables:
                # check that this is a positive sum to produce a greater than
                if all([val > 0 for _, val in unknowns]) or all(
                    [val < 0 for _, val in unknowns]
                ):
                    divisor = equation[free_variables[0]]
                    if free_variables[0] in ranges:
                        if ranges[free_variables[0]][1] == 0:
                            ranges[free_variables[0]] = [
                                ranges[free_variables[0]][0],
                                math.ceil(equation[-1] / divisor),
                            ]
                        elif (
                            math.ceil(equation[-1] / divisor)
                            < ranges[free_variables[0]][1]
                        ):
                            ranges[free_variables[0]] = [
                                ranges[free_variables[0]][0],
                                math.ceil(equation[-1] / divisor),
                            ]
                    else:
                        ranges[free_variables[0]] = [
                            0,
                            math.ceil(equation[-1] / divisor),
                        ]
                # if there's a minimum
                else:
                    divisor = equation[free_variables[0]]
                    if free_variables[0] in ranges:
                        if ranges[free_variables[0]][0] == 0:
                            ranges[free_variables[0]] = [
                                math.ceil(equation[-1] / divisor),
                                ranges[free_variables[0]][1],
                            ]
                        elif (
                            math.ceil(equation[-1] / divisor)
                            > ranges[free_variables[0]][0]
                        ):
                            ranges[free_variables[0]] = [
                                math.ceil(equation[-1] / divisor),
                                ranges[free_variables[0]][1],
                            ]
                    else:
                        ranges[free_variables[0]] = [
                            math.ceil(equation[-1] / divisor),
                            0,
                        ]
        for free_variable in free:
            if free_variable not in ranges.keys():
                presses = self.buttons[free_variable]
                range = min([self.joltage[button] for button in presses])
                ranges[free_variable] = [0, int(range)]
            # if upper range is zero then fill in as above
            elif ranges[free_variable][1] == 0:
                presses = self.buttons[free_variable]
                range = min([self.joltage[button] for button in presses])
                ranges[free_variable] = [ranges[free_variable][0], int(range)]
        for key, val in ranges.items():
            if val[0] < 0:
                ranges[key] = [0, val[1]]
        ranges = {key: val for key, val in ranges.items() if key in free}
        return ranges, free

    def find_solutions(self, free, ranges):
        total_presses = 1e10
        for indices in product(
            *(range(val[0], val[1] + 1) for _, val in ranges.items())
        ):
            partial_solution = [None] * (len(self.equations[0]) - 1)
            for i in range(len(indices)):
                partial_solution[free[i]] = indices[i]
            check_equations = self.equations[::-1].copy()
            not_solved = []
            solved_variable = False
            for num, equation in enumerate(check_equations):
                equation_solution = [
                    x * y
                    for x, y in zip(equation[:-1], partial_solution)
                    if y is not None
                ]
                unknowns = [
                    (num, x)
                    for num, x in enumerate(equation[:-1])
                    if partial_solution[num] == None and x != 0
                ]
                if len(unknowns) == 0:
                    if sum(equation_solution) != equation[-1]:
                        break
                    else:
                        continue
                if len(unknowns) == 1:
                    solution = (equation[-1] - sum(equation_solution)) / unknowns[0][1]
                    if solution >= 0:
                        variable = unknowns[0][0]
                        partial_solution[variable] = int(solution)
                        solved_variable = True
                else:
                    not_solved.append(num)
            if solved_variable:
                if len(not_solved) > 0:
                    check_equations = [
                        equation
                        for num, equation in enumerate(self.equations[::-1])
                        if num in not_solved
                    ]
                elif None not in partial_solution:
                    if sum(partial_solution) < total_presses:
                        total_presses = sum(partial_solution)
            if not solved_variable and len(not_solved) > 0:
                continue

        return total_presses

    def minimum_joltage_presses(self, debug=False):
        self.joltage_equation_system()
        if debug:
            print(
                f"Equations: {"\n".join(str(equation) for equation in self.equations)}"
            )
        self.row_echelon()
        if debug:
            print(
                f"Echelon = {"\n".join(str(equation) for equation in self.equations)}"
            )
        self.reduced_row_echelon()
        if debug:
            print(
                f"Reduced = {"\n".join(str(equation) for equation in self.equations)}"
            )
        free = self.find_free_variables()
        ranges, free = self.range_for_free(free)
        if debug:
            print(f"{ranges=}")
        return self.find_solutions(free, ranges)


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


assert test_machine_1.joltage_equation_system() == [
    [1, 1, 0, 1, 0, 0, 7],
    [0, 1, 0, 0, 0, 1, 5],
    [0, 0, 1, 1, 1, 0, 4],
    [0, 0, 0, 0, 1, 1, 3],
]
assert test_machine_1.row_echelon() == [
    [1, 1, 0, 1, 0, 0, 7],
    [0, 1, 0, 0, 0, 1, 5],
    [0, 0, 1, 1, 1, 0, 4],
    [0, 0, 0, 0, 1, 1, 3],
]

test_machine_1.reset_equations()

assert test_machine_1.minimum_joltage_presses() == 10
assert test_machine_2.minimum_joltage_presses() == 11

test_machine_3 = test_machines[1]
assert test_machine_3.joltage_equation_system() == [
    [1, 1, 0, 1, 1, 12],
    [1, 1, 0, 0, 1, 7],
    [1, 0, 1, 1, 0, 7],
    [1, 0, 1, 0, 1, 2],
    [0, 0, 0, 1, 1, 5],
]

test_machine_3.reset_equations()

assert test_machine_3.minimum_joltage_presses() == 12


def minimum_joltage_all_machines(data, debug=False):
    machines = parse_data(data)
    presses = 0
    if debug:
        for num, machine in enumerate(machines):
            if num > 13:
                print(f"\n\nChecking machine {num+1}")
                min_presses = machine.minimum_joltage_presses()
                if min_presses == 1e10:
                    print("No solution found")
                    # break
                else:
                    print(f"{machine.indicator=},{min_presses=}")
    else:
        for machine in machines:
            presses += machine.minimum_joltage_presses()
    return presses


assert minimum_joltage_all_machines(test_data, debug=False) == 33

test_machine_4 = parse_data("[.#.#.] (0,2,3,4) (1,3) (0,2) (1,4) {1,27,1,7,20}")[0]
print(test_machine_4.minimum_joltage_presses())

test_machine_5 = parse_data(
    "[.....#.#.] (3,4) (1,4) (0,2,3,5,6,8) (1,4,5,7) (0,3,4,6,7,8) (0,1,2,3,5,8) (2,4,5) (2,5) (2,3,5,8) (6) {24,29,22,43,58,28,19,16,24}"
)[0]
print(test_machine_5.minimum_joltage_presses())

test_machine_6 = parse_data(
    "[##......#.] (1,3,5,6,7,8) (1,2,6,7) (0,6) (0,3,4,5,6,8) (4,9) (0,1,2,3,4,5,6,7,8) (0,3,4,6,8,9) (1,4,6,7) (0,4) (1,2,4,5,8) (1,2,5) {38,41,30,18,50,30,44,27,31,4}"
)[0]
print(test_machine_6.minimum_joltage_presses())

test_machine_7 = parse_data(
    "[##....] (0,1,2,3,5) (0,1,2,4) (2,4) (1,3) (0,1,3) {26,42,18,40,7,11}"
)[0]
print(test_machine_7.minimum_joltage_presses(debug=True))

test_machine_8 = parse_data(
    "[.#..#.#] (2,6) (2,3,5,6) (0,1,2,3,4,5) (0,1,6) (0,5) (0,3,4,5,6) (1,3,4) {48,51,46,56,47,41,56}"
)[0]
print(test_machine_8.minimum_joltage_presses())

test_machine_9 = parse_data(
    "[###..#####] (1,2,4,5,6,7,8) (0,1,2,5,6,7,8,9) (2,4) (0,4,6,8) (2,3,4,6,9) (1,3,4,5,6,7,8,9) (0,1,2,3,6,7,9) (2,4,5,6,7) {23,34,192,173,193,28,192,41,26,178}"
)[0]
print(test_machine_9.minimum_joltage_presses())

test_machine_10 = parse_data(
    "[..###.#..] (0,2,5,7) (0,1,3,5,6) (4) (1,8) (0,1,4,6,7,8) (0,2,3,6) (0,1,2,6,7,8) (0,1,2,5,6,7) (1,5,7,8) {36,67,25,6,25,27,31,48,63}"
)[0]
print(test_machine_10.minimum_joltage_presses())

answer_2 = minimum_joltage_all_machines(input_data, debug=True)
print(answer_2)


# slow: 14
# incorrect: 92,173
