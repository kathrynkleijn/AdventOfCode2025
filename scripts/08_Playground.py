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

    def __init__(self, *junctions):
        self.junctions = junctions


class Circuit:

    def __init__(self, junctions=[]):
        self.junctions = junctions
        self.size = len(self.junctions)

    def add_junctions(self, *junctions):
        list(set(self.junctions.extend([junctions])))


def calculate_distance(junction1, junciton2):
    return math.sqrt(
        sum([(x - y) ** 2 for x, y in zip(junction1.coords, junciton2.coords)])
    )


def parse_data(data):
    junctions = []
    for junction in data.split("\n"):
        junctions.append(JunctionBox(junction))
    return junctions


def find_minimum_distance(data, previous=0):
    min_dist = 1e10
    for junction1, junction2 in product(parse_data(data), parse_data(data)):
        if junction1 != junction2:
            dist = calculate_distance(junction1, junction2)
            if dist < min_dist and dist > previous:
                min_dist = dist
                pair = (junction1, junction2)
    return pair, min_dist


test_junction1 = JunctionBox("162,817,812")
test_junction2 = JunctionBox("425,690,689")


assert find_minimum_distance(test_data) == (
    (test_junction1, test_junction2),
    calculate_distance(test_junction1, test_junction2),
)


def find_distances(data):
    distances = defaultdict()
    for junction1, junction2 in product(parse_data(data), parse_data(data)):
        if junction1 != junction2:
            distances[calculate_distance(junction1, junction2)] = (junction1, junction2)
    return distances


def find_minimum(distances, previous=0):
    last_pair = [pair for dist, pair in distances.items() if dist == previous]
    if last_pair:
        distances.pop(last_pair[0])
    return min([(dist, pair) for dist, pair in distances.items()])


test_distances = find_distances(test_data)
assert find_minimum(test_distances) == (
    (
        calculate_distance(test_junction1, test_junction2),
        (test_junction2, test_junction1),
    )
)


def find_connections(num_connections, data):
    circuits = []
    distances = find_distances(data)
    previous = 0
    for _ in range(num_connections):
        previous, pair = find_minimum(distances, previous)
        junction1, junction2 = pair
        added = False
        for circuit in circuits:
            if junction1 or junction2 in circuit:
                circuit.add_junctions(pair)
                added = True
                break
        if not added:
            circuits.append(Circuit(list(pair)))
