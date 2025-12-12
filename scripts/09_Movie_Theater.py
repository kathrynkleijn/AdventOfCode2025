## Day 9: Movie Theater

from itertools import combinations_with_replacement
from operator import itemgetter

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
    return sorted(
        [(int(coord.split(",")[0]), int(coord.split(",")[1])) for coord in coords]
    )


assert parse_data(test_data.split("\n")) == [
    (2, 3),
    (2, 5),
    (7, 1),
    (7, 3),
    (9, 5),
    (9, 7),
    (11, 1),
    (11, 7),
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


def possible_pairings(coords):
    possible = {}
    # assumes current coordinate is top left-hand corner of rectangle
    for test_coord in coords:
        col, row = test_coord[0], test_coord[1]
        check_list = [coord for coord in coords if coord != test_coord]
        # is there another coordinate with the same column or before, and a larger row?
        smaller_cols = [
            coord for coord in check_list if (coord[0] <= col) and (coord[1] > row)
        ]
        if smaller_cols:
            # the bottom left corner exists
            # if we hit something in the same column, then there will be a hole beneath it - remove anything
            # in a row that is larger than the first row for our column
            sorted_cols = sorted(smaller_cols, key=itemgetter(1))
            first_test_col = sorted(
                [coord for coord in smaller_cols if coord[0] == col], key=itemgetter(1)
            )
            if first_test_col:
                first_test_col = first_test_col[0]
                index = sorted_cols.index(first_test_col)
            else:
                index = len(sorted_cols) - 1
            # what's the largest row for these coordinates? this is the largest bottom right corner
            check_row = max([coord[1] for coord in sorted_cols[: index + 1]])
            # is there another coordinate with the same row or before, and a larger column?
            smaller_rows = [
                coord for coord in check_list if (coord[1] <= row) and (coord[0] > col)
            ]
            if smaller_rows:
                # the top right corner exists
                # what's the largest column for these coordinates? this is the largest top left corner
                sorted_rows = sorted(smaller_rows, key=itemgetter(1))
                first_test_row = sorted(
                    [coord for coord in smaller_rows if coord[1] == row],
                    key=itemgetter(1),
                )
                if first_test_row:
                    first_test_row = first_test_row[0]
                    index = sorted_rows.index(first_test_row)
                else:
                    index = len(sorted_rows) - 1
                check_col = max([coord[0] for coord in sorted_rows[: index + 1]])
                # keep any coordinates that fall in the range of the largest corners
                check_col_list = [
                    coord
                    for coord in check_list
                    if col <= coord[0] <= check_col and row <= coord[1] <= check_row
                ]
                if check_col_list:
                    possible[test_coord] = check_col_list
    return possible


def calulate_max_area_with_green(all_coords):
    max_area = 0
    x_distances, y_distances = distances(all_coords)
    possible = possible_pairings(all_coords)
    for test_coord, check_list in possible.items():
        max_area = area_loop(check_list, test_coord, x_distances, y_distances, max_area)
    return max_area


assert calulate_max_area_with_green(test_coords) == 24

answer_2 = calulate_max_area_with_green(answer_coords)
print(answer_2)

# smaller than previous but still higher than second #too large commit
# what about (7,3) and (11,1)? A rectangle is possible here too.
# there could be holes - bottom right hand corner is not correct - check from bottom left hand corner where maximum column is?
