## Day 7: Laboratories

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


class TachyonManifold:

    def __init__(self, map, debug=False):
        self.map = map
        self.rows = self.map.split("\n")
        self.grid = self.to_grid()
        self.m = len(self.rows)
        self.n = len(self.rows[0])
        self.size = (self.m, self.n)
        self.start = self.start_point()
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


test_manifold = TachyonManifold(test_data, debug=True)
print(test_manifold)

assert test_manifold.start == (1, 7)

assert test_manifold.beam_step_through() == 21
