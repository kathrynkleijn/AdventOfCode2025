## Day 7: Laboratories

from collections import defaultdict

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

    def count_splits(self):
        first_row = self.start[0] + 1
        splitter_count = defaultdict(lambda: 1)
        splitter_dict = defaultdict(list)
        for i in self.splitters[::-1]:
            splitter_dict[i[0]].append(i[1])
        for key, cols in splitter_dict.items():
            for col in cols:
                for row in reversed(range(first_row, key, 2)):
                    if col in splitter_dict[row]:
                        splitter_count[(row, col)] += splitter_count[(key, col)] - 1
                        splitter_count[(key, col)] = 0
                    elif col - 1 in splitter_dict[row]:
                        splitter_count[(row, col - 1)] += splitter_count[(key, col)]
                        break
                    elif col + 1 in splitter_dict[row]:
                        splitter_count[(row, col + 1)] += splitter_count[(key, col)]
                        break
        if self.debug:
            print(splitter_count)
        top_splitter = splitter_dict[first_row][0]
        return splitter_count[(first_row, top_splitter)]


test_manifold = TachyonManifold(test_data, debug=True)
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


test_manifold2 = TachyonManifold(test_data2, debug=True)
assert test_manifold2.beam_step_through() == test_manifold2.count_splits()

test_manifold3 = TachyonManifold(test_data3, debug=True)
assert test_manifold3.beam_step_through() == test_manifold3.count_splits()


with open("../input_data/07_Laboratories.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_manifold = TachyonManifold(input_data)
print(answer_manifold.count_splits())
