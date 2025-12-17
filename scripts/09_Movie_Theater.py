## Day 9: Movie Theater

from itertools import combinations_with_replacement
from operator import itemgetter
from collections import defaultdict

# Part 1

test_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def parse_data(coords):
    return [(int(coord.split(",")[0]), int(coord.split(",")[1])) for coord in coords]


assert parse_data(test_data.split("\n")) == [
    (7, 1),
    (11, 1),
    (11, 7),
    (9, 7),
    (9, 5),
    (2, 5),
    (2, 3),
    (7, 3),
]


def x_y_coordinates(coords, i="xy"):
    if i == "x":
        return set([x for x, _ in coords])
    elif i == "y":
        return set([y for _, y in coords])
    return set([x for x, _ in coords]), set([y for _, y in coords])


def distance_between(i_coords):
    distances = {}
    for i, j in combinations_with_replacement(i_coords, 2):
        if i != j:
            distances[(i, j)] = abs(j - i) + 1
            distances[(j, i)] = abs(i - j) + 1
    return distances


def distances(coords):
    x_coords, y_coords = x_y_coordinates(coords)
    return distance_between(x_coords), distance_between(y_coords)


def area_loop(check_list, test_coord, x_distances, y_distances, max_area):
    for coord in check_list:
        # print(f"{coord=},{test_coord=},{max_area=}")
        if coord[0] != test_coord[0]:
            x_dist = x_distances[(test_coord[0], coord[0])]
            if coord[1] != test_coord[1]:
                y_dist = y_distances[(test_coord[1], coord[1])]
            else:
                y_dist = 1
        else:
            x_dist = 1
            y_dist = y_distances[(test_coord[1], coord[1])]
        if x_dist * y_dist > max_area:
            max_area = x_dist * y_dist
            # print(f"bigger, {max_area=}")
        # print(f"{max_area=}")
    return max_area


def calculate_max_area(coords):
    max_area = 0
    x_distances, y_distances = distances(coords)
    check_list = coords.copy()
    for test_coord in coords:
        check_list = [coord for coord in check_list if coord != test_coord]
        max_area = area_loop(check_list, test_coord, x_distances, y_distances, max_area)
    return max_area


test_coords = parse_data(test_data.split("\n"))
assert calculate_max_area(test_coords) == 50


with open("../input_data/09_Movie_Theater.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_coords = parse_data(input_data.split("\n"))
answer_1 = calculate_max_area(answer_coords)
print(answer_1)

# Part 2

test_data2 = """4,2
13,2
13,4
8,4
8,6
11,6
11,10
4,10"""

test_data3 = """3,2
13,2
13,4
8,4
8,6
11,6
11,11
7,11
7,8
5,8
5,10
3,10"""

test_data4 = """3,2
17,2
17,13
13,13
13,11
15,11
15,8
11,8
11,15
18,15
18,17
4,17
4,12
6,12
6,5
3,5"""


def connections(coords):
    connection_dict = {}
    green_coords = []
    x_coords, y_coords = x_y_coordinates(coords)
    col_prev, row_prev = coords[-1]
    coord = coords[0]
    col, row = coord
    # where is it coming from?
    if row == row_prev:
        if col > col_prev:
            connection_dict[coord] = ["L"]
        elif col < col_prev:
            connection_dict[coord] = ["R"]
    elif col == col_prev:
        if row > row_prev:
            connection_dict[coord] = ["D"]
        elif row < row_prev:
            connection_dict[coord] = ["U"]
    for num, coord in enumerate(coords):
        col, row = coord
        if num < len(coords) - 1:
            col_next, row_next = coords[num + 1]
        else:
            col_next, row_next = coords[0]
        if num > 0:
            connection_dict[coord] = list(connection_dict[coords[num - 1]][-1])
        # where is it going to? add greens in between
        if row_next == row:
            if col_next > col:
                connection_dict[coord].append("R")
                for i in range(col + 1, col_next):
                    if i in x_coords:
                        green_coords.append((i, row))
                        connection_dict[(i, row)] = ["R", "R"]
            elif col_next < col:
                connection_dict[coord].append("L")
                for i in range(col_next + 1, col):
                    if i in x_coords:
                        green_coords.append((i, row))
                        connection_dict[(i, row)] = ["L", "L"]
        elif col_next == col:
            if row_next > row:
                connection_dict[coord].append("D")
                for i in range(row + 1, row_next):
                    if i in y_coords:
                        green_coords.append((col, i))
                        connection_dict[(col, i)] = ["D", "D"]
            elif row_next < row:
                connection_dict[coord].append("U")
                for i in range(row_next + 1, row):
                    if i in y_coords:
                        green_coords.append((col, i))
                        connection_dict[(col, i)] = ["U", "U"]
        col_prev, row_prev = col, row
    return connection_dict, green_coords


def possible_pairings(coords, debug=False):
    belowright_exists = [
        ["U", "R"],
        ["D", "R"],
        ["U", "U"],
        ["R", "R"],
        ["U", "L"],
        ["R", "U"],
    ]
    belowleft_exists = [
        ["D", "D"],
        ["D", "R"],
        ["L", "D"],
        ["R", "R"],
        ["R", "U"],
        ["R", "D"],
    ]
    connection_dict, green_coords = connections(coords)
    all_coords = coords + green_coords
    possible = defaultdict(list)

    for test_coord in coords:
        col, row = test_coord[0], test_coord[1]

        # assume current coordinate is top left-hand corner of rectangle
        # which direction is the circuit coming from and going to? if no greens to right and below, skip
        if connection_dict[test_coord] in belowright_exists:
            check_list = [coord for coord in all_coords if coord != test_coord]
            # what is the first row we hit in this column that will have a hole beneath?
            # the largest bottom left-hand corner is this coordinate
            left_corner = sorted(
                [
                    coord
                    for coord in check_list
                    if (coord[0] == col)
                    and connection_dict[coord][0] == "L"
                    and coord[1] > row
                ],
                key=itemgetter(1),
            )[0]
            # what is the first row we hit in this row that will have a hole next to it?
            # the largest top right-hand corner is this coordinate
            right_corner = sorted(
                [
                    coord
                    for coord in check_list
                    if (coord[1] == row) and connection_dict[coord][1] == "D"
                ]
            )[0]
            if debug:
                print(f"below right, {test_coord=}")
                print(f"{left_corner=}")
                print(f"{right_corner=}")

            # keep any coordinates that fall in the range of the largest corners
            keep_list = [coord for coord in coords if coord != test_coord]
            largest_row = left_corner[1]
            largest_col = right_corner[0]

            # rectangles on single line
            straight_line_list = [
                coord
                for coord in keep_list
                if (coord[0] == col and row < coord[1] <= largest_row)
                or (coord[1] == row and col < coord[0] <= largest_col)
            ]
            if debug:
                print(f"{straight_line_list=}")
            if straight_line_list:
                possible[test_coord].extend(straight_line_list)

            # other rectangles
            non_line_list = sorted(
                [
                    coord
                    for coord in keep_list
                    if col < coord[0] <= largest_col and row < coord[1] <= largest_row
                ]
            )
            if debug:
                print(f"{non_line_list=}")

            # check no hole beneath for each coordinate and remove others beyond
            for coord in non_line_list:
                if connection_dict[coord] not in belowright_exists:
                    limit_col, limit_row = coord
                    non_line_list = [
                        coord
                        for coord in non_line_list
                        if (coord[0] <= limit_col) or (coord[1] <= limit_row)
                    ]
            if debug:
                print(f"{non_line_list=}")
            if non_line_list:
                possible[test_coord].extend(non_line_list)

        # assume current coordinate is top right-hand corner of rectangle
        # which direction is the circuit coming from and going to? if no greens to left and below, skip
        if connection_dict[test_coord] in belowleft_exists:
            check_list = [coord for coord in all_coords if coord != test_coord]
            # what is the first row we hit in this column that will have a hole beneath?
            # the largest bottom right-hand corner is this coordinate
            right_corner = sorted(
                [
                    coord
                    for coord in check_list
                    if (coord[0] == col)
                    and connection_dict[coord][1] == "L"
                    and coord[1] > row
                ],
                key=itemgetter(1),
            )[0]
            # what is the first column we hit in this row that will have a hole next to it?
            # the largest top left-hand corner is this coordinate
            left_corner = sorted(
                [
                    coord
                    for coord in check_list
                    if (coord[1] == row) and connection_dict[coord][0] == "U"
                ]
            )[-1]

            if debug:
                print(f"below left, {test_coord=}")
                print(f"{left_corner=}")
                print(f"{right_corner=}")

            # keep any coordinates that fall in the range of the largest corners
            keep_list = [coord for coord in coords if coord != test_coord]
            largest_row = right_corner[1]
            largest_col = left_corner[0]

            # rectangles on single line
            straight_line_list = [
                coord
                for coord in keep_list
                if (coord[0] == col and row < coord[1] <= largest_row)
                or (coord[1] == row and largest_col <= coord[0] < col)
            ]
            if debug:
                print(f"{straight_line_list=}")
            if straight_line_list:
                possible[test_coord].extend(straight_line_list)

            # other rectangles
            non_line_list = sorted(
                [
                    coord
                    for coord in keep_list
                    if largest_col <= coord[0] < col and row < coord[1] <= largest_row
                ]
            )
            if debug:
                print(f"{non_line_list=}")

            # check no hole beneath for each coordinate and remove others beyond
            for coord in non_line_list:
                if connection_dict[coord] not in belowleft_exists:
                    limit_col, limit_row = coord
                    non_line_list = [
                        coord
                        for coord in non_line_list
                        if (coord[0] >= limit_col) or (coord[1] <= limit_row)
                    ]
            if debug:
                print(f"{non_line_list=}")
            if non_line_list:
                possible[test_coord].extend(non_line_list)

    # assume any other single line rectangles are smaller and don't bother chekcing
    if debug:
        print(possible)
    return possible


def calulate_max_area_with_green(all_coords, debug=False):
    max_area = 0
    x_distances, y_distances = distances(all_coords)
    possible = possible_pairings(all_coords, debug)
    for test_coord, check_list in possible.items():
        # print(f"{test_coord=},{max_area=}")
        max_area = area_loop(check_list, test_coord, x_distances, y_distances, max_area)
    return max_area


assert calulate_max_area_with_green(test_coords) == 24

test_coords2 = parse_data(test_data2.split("\n"))
test_coords3 = parse_data(test_data3.split("\n"))
test_coords4 = parse_data(test_data4.split("\n"))

assert calulate_max_area_with_green(test_coords2) == 40
assert calulate_max_area_with_green(test_coords3) == 35
assert calulate_max_area_with_green(test_coords4) == 66

answer_2 = calulate_max_area_with_green(answer_coords)
print(answer_2)
