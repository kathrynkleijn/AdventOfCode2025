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
        self.size = len(self.junctions)
        self.distances = self.find_distances()
        self.circuits = []
        self.debug = debug

    def __str__(self):
        return " ".join([str(junction) for junction in self.junctions])

    def calculate_distance(self, junction1, junciton2):
        return sum([(x - y) ** 2 for x, y in zip(junction1.coords, junciton2.coords)])

    def find_distances(self):
        self.distances = defaultdict()
        for junction1, junction2 in product(self.junctions, self.junctions):
            if junction1 != junction2:
                self.distances[self.calculate_distance(junction1, junction2)] = (
                    junction1,
                    junction2,
                )
        return dict(sorted(self.distances.items()))

    def find_connections(self, num_connections):
        for dist, pair in list(self.distances.items())[:num_connections]:
            if self.debug:
                print(f"{pair=}")
            junction1, junction2 = pair
            added = False
            for circuit in self.circuits:
                if not added:
                    if circuit.is_in_circuit(junction1) or circuit.is_in_circuit(
                        junction2
                    ):
                        circuit.add_junctions(list(pair))
                        added = True
                        containing_circuit = circuit
                else:
                    if circuit.is_in_circuit(junction1) or circuit.is_in_circuit(
                        junction2
                    ):
                        circuit.merge_circuits(containing_circuit)
                        self.circuits.remove(containing_circuit)
            if not added:
                self.circuits.append(Circuit(list(pair)))
            if self.debug:
                print([str(circuit) for circuit in self.circuits])
        return sorted([circuit.size for circuit in self.circuits])

    def largest_multiplied(self, num_connections):
        sizes = self.find_connections(num_connections)[::-1]
        return math.prod(sizes[:3])

    def reset(self):
        self.distances = self.find_distances()
        self.circuits = []

    def connect_all(self):
        # add first circuit
        dist, pair = list(self.distances.items())[0]
        self.circuits.append(Circuit(list(pair)))
        # add circuits until there is only one left over
        count = 1
        while len(self.circuits) > 1 or self.circuits[0].size < self.size - 1:
            dist, pair = list(self.distances.items())[count]
            junction1, junction2 = pair
            added = False
            for circuit in self.circuits:
                if not added:
                    if circuit.is_in_circuit(junction1):
                        circuit.add_junctions([junction2])
                        added = True
                        containing_circuit = circuit

                    elif circuit.is_in_circuit(junction2):
                        circuit.add_junctions([junction1])
                        added = True
                        containing_circuit = circuit

                else:
                    if circuit.is_in_circuit(junction1) or circuit.is_in_circuit(
                        junction2
                    ):
                        circuit.merge_circuits(containing_circuit)
                        self.circuits.remove(containing_circuit)
            if not added:
                self.circuits.append(Circuit(list(pair)))
            count += 1
        for junction in self.junctions:
            if not self.circuits[0].is_in_circuit(junction):
                distances = sorted(
                    [
                        (dist, pair)
                        for dist, pair in self.distances.items()
                        if junction in pair
                    ]
                )
                min_dist, pair = distances[0]
        junction1, junction2 = pair
        if self.debug:
            print(pair)
        return junction1.x * junction2.x


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

    def merge_circuits(self, circuit):
        self.add_junctions(circuit.junctions)


test_set_2 = SetOfJunctions(test_data.split("\n"))

assert test_set_2.find_connections(10) == [2, 2, 4, 5]
test_set_2.reset()
assert test_set_2.largest_multiplied(10) == 40


with open("../input_data/08_Playground.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_set = SetOfJunctions(input_data.split("\n"))
print(answer_set.largest_multiplied(1000))


# Part 2

test_set_2.reset()
assert test_set_2.connect_all() == 25272

answer_set.reset()
print(answer_set.connect_all())
