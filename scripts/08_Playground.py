## Day 8: Playground

import math
from itertools import combinations_with_replacement, product
from collections import defaultdict
import time

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
        self.pairs = self.find_distances()
        self.circuits = SetOfCircuits(Circuit)
        self.debug = debug

    def __str__(self):
        return " ".join([str(junction) for junction in self.junctions])

    def calculate_distance(self, junction1, junciton2):
        return sum([(x - y) ** 2 for x, y in zip(junction1.coords, junciton2.coords)])

    def find_distances(self):
        distances = defaultdict()
        for junction1, junction2 in combinations_with_replacement(self.junctions, 2):
            if junction1 != junction2:
                distances[self.calculate_distance(junction1, junction2)] = (
                    junction1,
                    junction2,
                )
        return [pair for _, pair in dict(sorted(distances.items())).items()]

    def find_connections(self, num_connections):
        connected = defaultdict(set)
        count = 0
        for pair in self.pairs[:num_connections]:
            if self.debug:
                print(f"{pair=}")
            junction1, junction2 = pair
            if connected[str(junction1)]:
                circuit = list(connected[str(junction1)])[0]
                self.circuits[circuit].add_junctions([junction2])
                connected[str(junction2)].add(circuit)
                if len(connected[str(junction2)]) > 1:
                    first_circuit, second_circuit = list(connected[str(junction2)])
                    if len(self.circuits[first_circuit]) >= len(
                        self.circuits[second_circuit]
                    ):
                        self.circuits[first_circuit].merge_circuits(
                            self.circuits[second_circuit]
                        )
                        del self.circuits[second_circuit]
                        for junction in self.circuits[first_circuit]:
                            connected[str(junction)] = {first_circuit}
                    else:
                        self.circuits[second_circuit].merge_circuits(
                            self.circuits[first_circuit]
                        )
                        del self.circuits[first_circuit]
                        for junction in self.circuits[second_circuit]:
                            connected[str(junction)] = {second_circuit}
            elif connected[str(junction2)]:
                circuit = list(connected[str(junction2)])[0]
                self.circuits[circuit].add_junctions([junction1])
                connected[str(junction1)].add(circuit)
            else:
                self.circuits[count] = Circuit(count, list(pair))
                connected[str(junction1)].add(count)
                connected[str(junction2)].add(count)
            count += 1
            if self.debug:
                print([str(circuit) for circuit in self.circuits.values()])
        return sorted([len(circuit) for circuit in self.circuits.values()])

    def largest_multiplied(self, num_connections):
        sizes = self.find_connections(num_connections)[::-1]
        return math.prod(sizes[:3])

    def reset(self):
        self.circuits = SetOfCircuits(Circuit)

    def connect_all(self):
        connected = defaultdict(set)
        # add first circuit
        pair = self.pairs[0]
        self.circuits[0] = Circuit(0, list(pair))
        junction1, junction2 = pair
        connected[str(junction1)].add(0)
        connected[str(junction2)].add(0)
        # add circuits until there is only one left over
        count = 1
        while (
            len(self.circuits.items()) > 1
            or len(list(self.circuits.values())[0]) < self.size - 1
        ):
            pair = self.pairs[count]
            junction1, junction2 = pair
            if connected[str(junction1)]:
                circuit = list(connected[str(junction1)])[0]
                self.circuits[circuit].add_junctions([junction2])
                connected[str(junction2)].add(circuit)
                if len(connected[str(junction2)]) > 1:
                    first_circuit, second_circuit = list(connected[str(junction2)])
                    if len(self.circuits[first_circuit]) >= len(
                        self.circuits[second_circuit]
                    ):
                        self.circuits[first_circuit].merge_circuits(
                            self.circuits[second_circuit]
                        )
                        del self.circuits[second_circuit]
                        for junction in self.circuits[first_circuit]:
                            connected[str(junction)] = {first_circuit}
                    else:
                        self.circuits[second_circuit].merge_circuits(
                            self.circuits[first_circuit]
                        )
                        del self.circuits[first_circuit]
                        for junction in self.circuits[second_circuit]:
                            connected[str(junction)] = {second_circuit}
            elif connected[str(junction2)]:
                circuit = list(connected[str(junction2)])[0]
                self.circuits[circuit].add_junctions([junction1])
                connected[str(junction1)].add(circuit)
            else:
                self.circuits[count] = Circuit(count, list(pair))
                connected[str(junction1)].add(count)
                connected[str(junction2)].add(count)
            count += 1
        for junction in self.junctions:
            if junction not in list(self.circuits.values())[0]:
                pair = [pair for pair in self.pairs[count:] if junction in pair][0]
        junction1, junction2 = pair
        if self.debug:
            print(pair)
        return junction1.x * junction2.x


class Circuit(list):

    def __init__(self, name, junctions=[]):
        super().__init__(junctions)
        self.name = name

    def __str__(self):
        return " ".join([str(junction) for junction in self])

    def add_junctions(self, junctions):
        for junction in junctions:
            if junction not in self:
                self.append(junction)
        return self

    def merge_circuits(self, circuit):
        self.add_junctions(circuit)


class SetOfCircuits(defaultdict):

    def __init__(self, default_factory=None):
        super().__init__(default_factory)


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
