# Day 4: Printing Department

import itertools


test_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

test_answer = """..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x."""


class PaperMap:

    def __init__(self, map, debug=False, debug_fine=False):
        self.map = map
        self.rows = self.map.split("\n")
        self.grid = self.to_grid()
        self.m = len(self.rows)
        self.n = len(self.rows[0])
        self.size = (self.m, self.n)
        self.debug = debug
        self.debug_fine = debug_fine

    def __str__(self):
        return "\n".join(row for row in self.rows)

    def to_grid(self):
        return [list(row) for row in self.rows]

    def adjacent_spaces(self, i, j):
        return (
            tup
            for tup in itertools.product(range(i - 1, i + 2), range(j - 1, j + 2))
            if tup != (i, j) and 0 <= tup[0] < self.m and 0 <= tup[1] < self.n
        )

    def access_search(self, removing=False):
        if removing:
            adjacent_roll = ["@"]
        else:
            adjacent_roll = ["@", "x"]
        accessible = 0
        for i in range(self.m):
            if "@" not in self.grid[i]:
                continue
            for j in range(self.n):
                inaccesible = False
                adjacent = 0
                if self.grid[i][j] == "@":
                    for x, y in self.adjacent_spaces(i, j):
                        if self.grid[x][y] in adjacent_roll:
                            adjacent += 1
                            if adjacent >= 4:
                                inaccesible = True
                                break
                    if not inaccesible:
                        self.grid[i][j] = "x"
                        accessible += 1
                        if self.debug_fine:
                            grid_repr = []
                            for row in self.grid:
                                grid_repr.append("".join(x for x in row))
                            print("\n".join(row for row in grid_repr))
                            print("\n")
        if self.debug:
            grid_repr = []
            for row in self.grid:
                grid_repr.append("".join(x for x in row))
            print("\n".join(row for row in grid_repr))
            print("\n")
        return accessible

    def access_with_removal(self):
        accessible = 0
        removed = 1
        while removed > 0:
            removed = self.access_search(removing=True)
            accessible += removed
        return accessible

    def reset_grid(self):
        self.grid = self.to_grid()


# Part 1

test_map = PaperMap(test_data)

assert test_map.access_search() == 13

with open("../input_data/04_Printing_Department.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_map = PaperMap(input_data)
print(answer_map.access_search())

# Part 2


test_map.reset_grid()
assert test_map.access_with_removal() == 43

answer_map.reset_grid()
print(answer_map.access_with_removal())


# Alternative

from collections import Counter


class PaperMapNew:

    def __init__(self, map, debug=False, debug_fine=False):
        self.map = map
        self.rows = self.map.split("\n")
        self.grid = self.to_grid()
        self.m = len(self.rows)
        self.n = len(self.rows[0])
        self.size = (self.m, self.n)
        self.debug = debug
        self.debug_fine = debug_fine

    def __str__(self):
        return "\n".join(row for row in self.rows)

    def to_grid(self):
        return [list(row) for row in self.rows]

    def subgrid(self, i, j):
        if i == 0 and 0 < j < self.m - 1:
            return self.grid[i][j - 1 : j + 2] + self.grid[i + 1][j - 1 : j + 2]
        elif i == 0 and j == self.m - 1:
            return self.grid[i][j - 1 : j + 1] + self.grid[i + 1][j - 1 : j + 1]
        elif j == 0 and 0 < i < self.n - 1:
            return (
                self.grid[i - 1][j : j + 2]
                + self.grid[i][j : j + 2]
                + self.grid[i + 1][j : j + 2]
            )
        elif j == 0 and i == self.n - 1:
            return self.grid[i - 1][j : j + 2] + self.grid[i][j : j + 2]
        elif i == 0 and j == 0:
            return self.grid[i][j : j + 2] + self.grid[i + 1][j : j + 2]
        elif i == self.n - 1 and 0 < j < self.m - 1:
            return self.grid[i - 1][j - 1 : j + 2] + self.grid[i][j - 1 : j + 2]
        elif j == self.m - 1 and 0 < i < self.n - 1:
            return (
                self.grid[i - 1][j - 1 : j + 1]
                + self.grid[i][j - 1 : j + 1]
                + self.grid[i + 1][j - 1 : j + 1]
            )
        elif i == self.n - 1 and j == self.m - 1:
            return self.grid[i - 1][j - 1 : j + 1] + self.grid[i][j - 1 : j + 1]
        else:
            return (
                self.grid[i - 1][j - 1 : j + 2]
                + self.grid[i][j - 1 : j + 2]
                + self.grid[i + 1][j - 1 : j + 2]
            )

    def access_search(self, removing=False):
        accessible = 0
        for i in range(self.m):
            if "@" not in self.grid[i]:
                continue
            for j in range(self.n):
                if self.grid[i][j] == "@":
                    subgrid = self.subgrid(i, j)
                    if removing:
                        if (Counter(subgrid)["@"] - 1) < 4:
                            self.grid[i][j] = "x"
                            accessible += 1
                    else:
                        if (Counter(subgrid)["@"] + Counter(subgrid)["x"] - 1) < 4:
                            self.grid[i][j] = "x"
                            accessible += 1
        if self.debug:
            grid_repr = []
            for row in self.grid:
                grid_repr.append("".join(x for x in row))
            print("\n".join(row for row in grid_repr))
            print("\n")
        return accessible

    def access_with_removal(self):
        accessible = 0
        removed = 1
        while removed > 0:
            removed = self.access_search(removing=True)
            accessible += removed
        return accessible

    def reset_grid(self):
        self.grid = self.to_grid()


test_map = PaperMapNew(test_data)
test_map.reset_grid()
assert test_map.access_search() == 13


answer_map = PaperMapNew(input_data)
answer_map.reset_grid()
print(answer_map.access_search())

answer_map.reset_grid()
print(answer_map.access_with_removal())
