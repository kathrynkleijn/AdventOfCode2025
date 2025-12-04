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

test_map = PaperMap(test_data, debug=True)

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
