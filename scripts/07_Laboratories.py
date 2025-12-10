## Day 7: Laboratories

from collections import defaultdict, Counter
from math import factorial

# Part 1

test_data = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


test_data2 = """..............................S..............................
.............................................................
..............................^..............................
.............................................................
.............................^.^.............................
.............................................................
............................^.^.^............................
.............................................................
...........................^...^.^...........................
.............................................................
..........................^.^.....^..........................
.............................................................
.........................^...^.^.^.^.........................
.............................................................
........................^...^.^.....^........................
.............................................................
.......................^.^.^.^...^...^.......................
............................................................."""


test_data3 = """..............................S..............................
.............................................................
..............................^..............................
.............................................................
.............................^.^.............................
.............................................................
............................^.^.^............................
.............................................................
...........................^...^.^...........................
.............................................................
..........................^.^.....^..........................
.............................................................
.........................^...^.^.^.^.........................
.............................................................
........................^...^.^.....^........................
.............................................................
.......................^.^.^.^...^...^.......................
.............................................................
......................^.^.^.^.^.^.^.^.^......................
............................................................."""

test_data4 = """......S........
...............
......^........
...............
.....^.^.......
...............
....^...^......
...............
...^..^.^......
...............
..^.^.^.^......
...............
.^.^...^.......
..............."""


class TachyonManifold:

    def __init__(self, map, debug=False):
        self.map = map
        self.rows = self.map.split("\n")
        self.grid = self.to_grid()
        self.m = len(self.rows)
        self.n = len(self.rows[0])
        self.size = (self.m, self.n)
        self.start = self.start_point()
        self.splitters = self.find_splitters()
        self.splitter_dict = self.make_splitter_dict()
        self.debug = debug

    def __str__(self):
        return "\n".join(row for row in self.rows)

    def to_grid(self):
        return [list(row) for row in self.rows]

    def start_point(self):
        start = 0
        for num, row in enumerate(self.rows):
            start = row.index("S")
            if start:
                break
        return (num + 1, start)

    def beam_step_through(self):
        beam_starts = [self.start]
        splits = []
        for i, j in beam_starts:
            for k in range(i + 1, self.m):
                if self.rows[k][j] == "^":
                    if j == 0:
                        beam_starts.append((k, j + 1))
                    elif j == self.n:
                        beam_starts.append((k, j - 1))
                    else:
                        beam_starts.extend([(k, j - 1), (k, j + 1)])
                    splits.append((k, j))
                    if self.debug:
                        self.grid[k][j - 1] = "|"
                        self.grid[k][j + 1] = "|"
                    break
                else:
                    if self.debug:
                        self.grid[k][j] = "|"
        if self.debug:
            grid_repr = []
            for row in self.grid:
                grid_repr.append("".join(x for x in row))
            print("\n\n")
            print("\n".join(row for row in grid_repr))
            print("\n")
        return len(set(splits))

    def find_splitters(self):
        splitters = []
        for num, row in enumerate(self.rows):
            splitters.extend(
                [(num, index) for index, val in enumerate(row) if val == "^"]
            )
        return splitters

    def make_splitter_dict(self):
        splitter_dict = defaultdict(list)
        for i in self.splitters[::-1]:
            splitter_dict[i[0]].append(i[1])
        return splitter_dict

    def count_splits(self):
        first_row = self.start[0] + 1
        splitter_count = defaultdict(lambda: 1)
        for key, cols in self.splitter_dict.items():
            for col in cols:
                for row in reversed(range(first_row, key, 2)):
                    if col in self.splitter_dict[row]:
                        if splitter_count[(key, col)] != 0:
                            splitter_count[(row, col)] += splitter_count[(key, col)] - 1
                            splitter_count[(key, col)] = 0
                    elif col - 1 in self.splitter_dict[row]:
                        splitter_count[(row, col - 1)] += splitter_count[(key, col)]
                        break
                    elif col + 1 in self.splitter_dict[row]:
                        splitter_count[(row, col + 1)] += splitter_count[(key, col)]
                        break
        if self.debug:
            print(splitter_count)
        top_splitter = self.splitter_dict[first_row][0]
        return splitter_count[(first_row, top_splitter)]


test_manifold = TachyonManifold(test_data)
print(test_manifold)

assert test_manifold.start == (1, 7)

assert test_manifold.beam_step_through() == 21

assert test_manifold.splitters == [
    (2, 7),
    (4, 6),
    (4, 8),
    (6, 5),
    (6, 7),
    (6, 9),
    (8, 4),
    (8, 6),
    (8, 10),
    (10, 3),
    (10, 5),
    (10, 9),
    (10, 11),
    (12, 2),
    (12, 6),
    (12, 12),
    (14, 1),
    (14, 3),
    (14, 5),
    (14, 7),
    (14, 9),
    (14, 13),
]

assert test_manifold.count_splits() == 21


test_manifold2 = TachyonManifold(test_data2)
assert test_manifold2.beam_step_through() == test_manifold2.count_splits()

test_manifold3 = TachyonManifold(test_data3)
assert test_manifold3.beam_step_through() == test_manifold3.count_splits()

test_manifold4 = TachyonManifold(test_data4)
assert test_manifold4.beam_step_through() == test_manifold4.count_splits()


with open("../input_data/07_Laboratories.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_manifold = TachyonManifold(input_data)
print(answer_manifold.count_splits())


# Part 2


class QuantumTachyonManifold(TachyonManifold):

    def __init__(self, map, debug=False):
        self.map = map
        self.rows = self.map.split("\n")
        self.grid = self.to_grid()
        self.m = len(self.rows)
        self.n = len(self.rows[0])
        self.size = (self.m, self.n)
        self.start = self.start_point()
        self.splitters = self.find_splitters()
        self.splitter_dict = self.make_splitter_dict()
        self.splitter_paths = defaultdict(int, {self.splitters[0]: 1})
        self.paths_populated = False
        self.debug = debug

    def splitter_path(self, splitter):
        index = self.splitters.index(splitter)
        for split in self.splitters[1 : index + 1]:
            count = 0
            if self.splitter_paths[split]:
                count = self.splitter_paths[split]
            else:
                key, col = split
                rows = [row for row in self.splitter_dict.keys() if row < key]
                for row in rows:
                    if col in self.splitter_dict[row]:
                        break
                    if col - 1 in self.splitter_dict[row]:
                        count += self.splitter_paths[(row, col - 1)]
                    if col + 1 in self.splitter_dict[row]:
                        count += self.splitter_paths[(row, col + 1)]
                self.splitter_paths[split] = count
        if self.debug:
            print(self.splitter_paths)
        return count

    def final_point_path(self, point):
        if not self.paths_populated:
            self.splitter_path(self.splitters[-1])
            self.paths_populated = True
        row, col = point
        count = 0
        for row in self.splitter_dict.keys():
            if col in self.splitter_dict[row]:
                break
            if col - 1 in self.splitter_dict[row]:
                count += self.splitter_paths[(row, col - 1)]
            if col + 1 in self.splitter_dict[row]:
                count += self.splitter_paths[(row, col + 1)]
        if self.debug:
            print(point, count)
        return count

    def total_paths(self):
        point_paths = 0
        last_row = self.m - 1
        for i in range(self.n):
            point_paths += self.final_point_path((last_row, i))
        return point_paths


test_quantum = QuantumTachyonManifold(test_data)

assert test_quantum.splitter_path((4, 6)) == 1
assert test_quantum.splitter_path((4, 8)) == 1
assert test_quantum.splitter_path((6, 7)) == 2
assert test_quantum.splitter_path((12, 2)) == 1
assert test_quantum.splitter_path((12, 12)) == 1
assert test_quantum.splitter_path((12, 6)) == 4


assert test_quantum.total_paths() == 40


answer_quantum = QuantumTachyonManifold(input_data)
print(answer_quantum.total_paths())
