## Day 8: Playground

import math
from itertools import product
from collections import defaultdict

# Part 1

test_data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


class JunctionBox:

    def __init__(self, coords_str):
        self.coords_str = coords_str
        self.coords = [int(x) for x in self.coords_str.split(",")]
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.z = self.coords[2]

    def __repr__(self):
        return self.coords_str

    def __eq__(self, other):
        if not isinstance(other, JunctionBox):
            return False
        return self.coords == other.coords


class SetOfJunctions:

    def __init__(self, junctions=[], debug=False):
        self.junctions = [JunctionBox(junction) for junction in junctions]
        self.distances = self.find_distances()
        self.circuits = []
        self.debug = debug

    def __str__(self):
        return " ".join([str(junction) for junction in self.junctions])

    def calculate_distance(self, junction1, junciton2):
        return math.sqrt(
            sum([(x - y) ** 2 for x, y in zip(junction1.coords, junciton2.coords)])
        )

    def find_distances(self):
        self.distances = defaultdict()
        for junction1, junction2 in product(self.junctions, self.junctions):
            if junction1 != junction2:
                self.distances[self.calculate_distance(junction1, junction2)] = (
                    junction1,
                    junction2,
                )
        return self.distances

    def find_minimum(self, previous=0):
        if previous:
            self.distances.pop(previous)
        return min([(dist, pair) for dist, pair in self.distances.items()])

    def find_connections(self, num_connections):
        previous = 0
        for _ in range(num_connections):
            previous, pair = self.find_minimum(previous)
            if self.debug:
                print(f"{pair=}")
            junction1, junction2 = pair
            added = False
            for circuit in self.circuits:
                # what if one is in one circuit and the other in another?
                if circuit.is_in_circuit(junction1) or circuit.is_in_circuit(junction2):
                    circuit.add_junctions(list(pair))
                    added = True
                    break
            if not added:
                self.circuits.append(Circuit(list(pair)))
            if self.debug:
                print([str(circuit) for circuit in self.circuits])
        return [circuit.size for circuit in self.circuits]


class Circuit:

    def __init__(self, junctions=[]):
        self.junctions = junctions
        self.size = len(self.junctions)

    def __str__(self):
        return " ".join([str(junction) for junction in self.junctions])

    def add_junctions(self, junctions):
        for junction in junctions:
            if junction not in self.junctions:
                self.junctions.append(junction)
        self.size = len(self.junctions)
        return self.junctions

    def is_in_circuit(self, junction):
        if junction in self.junctions:
            return True
        return False


test_junction1 = JunctionBox("162,817,812")
test_junction2 = JunctionBox("425,690,689")


test_set = SetOfJunctions(["162,817,812", "425,690,689"])

assert test_set.find_minimum() == (
    (
        316.90219311326956,
        (test_junction2, test_junction1),
    )
)

test_set_2 = SetOfJunctions(test_data.split("\n"), debug=True)
print(test_set_2.find_connections(10))
# assert sorted(test_set_2.find_connections(10)) == [2, 2, 4, 5]
