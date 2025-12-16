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


def possible_pairings(coords):
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
        # assumes current coordinate is top left-hand corner of rectangle
        # which direction is the circuit coming from and going to? if no greens to right and below, skip
        if connection_dict[test_coord] in belowright_exists:
            check_list = [coord for coord in all_coords if coord != test_coord]
            # is there another coordinate with the same column or before, and a larger row?
            smaller_cols = [
                coord for coord in check_list if (coord[0] <= col) and (coord[1] > row)
            ]
            if smaller_cols:
                # the bottom left corner exists
                # if we hit a green which is going sideways in same column,
                # then there might be a hole beneath it - remove anything with a bigger row than this
                sorted_cols = sorted(smaller_cols, key=itemgetter(1))
                greens = []
                for green_tile in green_coords:
                    if green_tile[0] == col and green_tile in smaller_cols:
                        if connection_dict[green_tile] == ["L", "L"]:
                            greens.append(green_tile)
                if greens:
                    tile = sorted(greens, key=itemgetter(1))[0]
                    index = sorted_cols.index(tile)
                else:
                    index = len(sorted_cols) - 1
                # what's the largest row for these coordinates? this is the largest bottom left corner
                check_row = max([coord[1] for coord in sorted_cols[: index + 1]])
                # is there another coordinate with the same row or before, and a larger column?
                smaller_rows = [
                    coord
                    for coord in check_list
                    if (coord[1] <= row) and (coord[0] > col)
                ]
                if smaller_rows:
                    # the top right corner exists
                    # if we hit a green which is going downwards in same row,
                    # then there might be a hole next to it - remove anything with a bigger column than this
                    sorted_rows = sorted(smaller_rows)
                    greens = []
                    for green_tile in green_coords:
                        if green_tile[1] == row and green_tile in smaller_rows:
                            if connection_dict[green_tile] == ["D", "D"]:
                                greens.append(green_tile)
                    if greens:
                        tile = sorted(greens)[0]
                        index = sorted_rows.index(tile)
                    else:
                        index = len(sorted_rows) - 1
                    # what's the largest column for these coordinates? this is the largest top left corner
                    check_col = max([coord[0] for coord in sorted_rows[: index + 1]])
                    # keep any coordinates that fall in the range of the largest corners
                    keep_list = [coord for coord in coords if coord != test_coord]

                    straight_line_list = [
                        coord
                        for coord in keep_list
                        if (coord[0] == col and row <= coord[1] <= check_row)
                        or (coord[1] == row and col <= coord[0] <= check_col)
                    ]
                    if straight_line_list:
                        possible[test_coord].extend(straight_line_list)
                    non_line_list = sorted(
                        [
                            coord
                            for coord in keep_list
                            if col < coord[0] <= check_col
                            and row < coord[1] <= check_row
                        ]
                    )
                    if non_line_list:
                        min_col = sorted(non_line_list)[0][0]
                        col_sort = [
                            coord for coord in non_line_list if coord[0] == min_col
                        ]
                        min_row = sorted(non_line_list, key=itemgetter(1))[0][1]
                        row_sort = [
                            coord for coord in non_line_list if coord[1] == min_row
                        ]
                        sorted_coords = list(set(col_sort + row_sort))
                        possible[test_coord].extend(sorted_coords)
                        # possible[test_coord].extend(non_line_list)

        # assumes current coordinate is top right-hand corner of rectangle
        # which direction is the circuit coming from and going to? if no greens to left and below, skip
        if connection_dict[test_coord] in belowleft_exists:
            check_list = [coord for coord in all_coords if coord != test_coord]
            # is there another coordinate with the same column or before, and a larger row?
            smaller_cols = [
                coord for coord in check_list if (coord[0] <= col) and (coord[1] > row)
            ]
            if smaller_cols:
                # the bottom right corner exists
                # if we hit another red in our column that is going sideways,
                # then there's a hole beneath and we should remove it
                sorted_cols = sorted(smaller_cols, key=itemgetter(1))
                first_test_col = sorted(
                    [coord for coord in smaller_cols if coord[0] == col],
                    key=itemgetter(1),
                )
                if first_test_col:
                    first_test_col = first_test_col[0]
                    index = sorted_cols.index(first_test_col)
                else:
                    index = len(sorted_cols) - 1
                sorted_cols = sorted_cols[: index + 1]

                # if we hit a green which is going sideways in same column,
                # then there might be a hole beneath it - remove anything with a bigger row than this
                greens = []
                for green_tile in green_coords:
                    if green_tile[0] == col and green_tile in smaller_cols:
                        if connection_dict[green_tile] == ["R", "R"]:
                            greens.append(green_tile)
                if greens:
                    tile = sorted(greens, key=itemgetter(1))[0]
                    index = sorted_cols.index(tile)
                else:
                    index = len(sorted_cols) - 1

                # what's the largest row for these coordinates? this is the largest bottom right corner
                check_row = max([coord[1] for coord in sorted_cols[: index + 1]])
                # is there another coordinate with the same row or before, and a smaller column?
                smaller_rows = [
                    coord
                    for coord in check_list
                    if (coord[1] <= row) and (coord[0] < col)
                ]
                if smaller_rows:
                    # the top left corner exists
                    sorted_rows = sorted(smaller_rows, key=itemgetter(1))
                    # if we hit another red in our row that is going upwards,
                    # then there's a hole beneath and we should remove it
                    first_test_row = sorted(
                        [coord for coord in smaller_rows if coord[1] == row],
                        key=itemgetter(1),
                    )
                    if first_test_row:
                        first_test_row = first_test_row[0]
                        index = sorted_rows.index(first_test_row)
                    else:
                        index = len(sorted_rows) - 1
                    # if we hit a green which is going upwards in same row,
                    # then there might be a hole next to it - remove anything with a smaller column than this
                    sorted_rows = sorted(smaller_rows)[::-1]
                    greens = []
                    for green_tile in green_coords:
                        if green_tile[1] == row and green_tile in smaller_rows:
                            if connection_dict[green_tile] == ["U", "U"]:
                                greens.append(green_tile)
                    if greens:
                        tile = sorted(greens)[-1]
                        index = sorted_rows.index(tile)
                    else:
                        index = len(sorted_rows) - 1
                    # what's the smallest column for these coordinates? this is the smallest top left corner
                    check_col = min([coord[0] for coord in sorted_rows[: index + 1]])
                    # keep any coordinates that fall in the range of the largest corners
                    keep_list = [coord for coord in coords if coord != test_coord]
                    straight_line_list = [
                        coord
                        for coord in keep_list
                        if (coord[0] == col and row <= coord[1] <= check_row)
                        or (coord[1] == row and check_col <= coord[0] <= col)
                    ]
                    if straight_line_list:
                        possible[test_coord].extend(straight_line_list)
                    non_line_list = sorted(
                        [
                            coord
                            for coord in keep_list
                            if check_col <= coord[0] < col
                            and row < coord[1] <= check_row
                        ]
                    )
                    if non_line_list:
                        max_col = sorted(non_line_list)[-1][0]
                        col_sort = [
                            coord for coord in non_line_list if coord[0] == max_col
                        ]
                        min_row = sorted(non_line_list, key=itemgetter(1))[0][1]
                        row_sort = [
                            coord for coord in non_line_list if coord[1] == min_row
                        ]
                        print(f"{test_coord=},{col_sort=},{row_sort=}")
                        sorted_coords = list(set(col_sort + row_sort))
                        possible[test_coord].extend(sorted_coords)
        # left-direction straight lines
        if connection_dict[test_coord] in [["L", "L"], ["L", "U"], ["D", "L"]]:
            index = coords.index(test_coord)
            # add next coordinate as possible pairing
            if index < len(coords) - 1:
                possible[test_coord].append(coords[index + 1])
            else:
                possible[test_coord].append(coords[0])
    print(possible)
    return possible


def calulate_max_area_with_green(all_coords):
    max_area = 0
    x_distances, y_distances = distances(all_coords)
    possible = possible_pairings(all_coords)
    for test_coord, check_list in possible.items():
        # print(f"{test_coord=},{max_area=}")
        max_area = area_loop(check_list, test_coord, x_distances, y_distances, max_area)
    return max_area


# assert calulate_max_area_with_green(test_coords) == 24

test_coords2 = parse_data(test_data2.split("\n"))
test_coords3 = parse_data(test_data3.split("\n"))
test_coords4 = parse_data(test_data4.split("\n"))

print(calulate_max_area_with_green(test_coords3))

assert calulate_max_area_with_green(test_coords2) == 40
# assert calulate_max_area_with_green(test_coords3) == 35
# assert calulate_max_area_with_green(test_coords4) == 66

# answer_2 = calulate_max_area_with_green(answer_coords)
# print(answer_2)
