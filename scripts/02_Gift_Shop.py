## Day 2: Gift Shop

import math

# Part 1

test_data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


def check_range(id_range):
    start, stop = id_range.split("-")[0], id_range.split("-")[1]
    invalid = 0
    invalid_sum = 0
    if len(start) % 2 == 0:
        id_length = len(start)
    elif len(stop) % 2 == 0:
        id_length = len(stop)
    else:
        return (0, 0)
    for id in range(int(start), int(stop) + 1):
        id_str = str(id)
        index = int(id_length / 2)
        if id_str[:index] == id_str[index:]:
            invalid += 1
            invalid_sum += id
    return invalid, invalid_sum


assert check_range("11-22") == (2, 33)
assert check_range("1000-1012") == (1, 1010)
assert check_range("998-1012") == (1, 1010)


def check_list(list_of_ranges, new=False):
    invalid = 0
    invalid_sum = 0
    for id_range in list_of_ranges:
        if not new:
            id_num, id_sum = check_range(id_range)
        elif new:
            id_num, id_sum = check_range2(id_range)
        invalid += id_num
        invalid_sum += id_sum
    return invalid, invalid_sum


assert check_list(test_data.strip().split(",")) == (8, 1227775554)

with open("../input_data/02_Gift_Shop.txt", "r", encoding="utf-8") as file:
    ranges = file.read().strip().split(",")

answer_1 = check_list(ranges)
print(answer_1)

# Part 2


def split_id(id, factor):
    return (id[0 + i : factor + i] for i in range(0, len(id), factor))


def find_factors(id_length):
    return (i for i in range(2, id_length) if id_length % i == 0)


def check_range2(id_range):
    start, stop = id_range.split("-")[0], id_range.split("-")[1]
    invalid = 0
    invalid_sum = 0
    for id in range(int(start), int(stop) + 1):
        id_length = len(str(id))
        if id_length == 1:
            continue
        elif len(set(split_id(str(id), 1))) == 1:
            invalid += 1
            invalid_sum += id
        else:
            for i in find_factors(id_length):
                if len(set(split_id(str(id), i))) == 1:
                    invalid += 1
                    invalid_sum += id
                    break
    return invalid, invalid_sum


assert check_range2("11-22") == (2, 33)
assert check_range2("1000-1012") == (1, 1010)
assert check_range2("998-1012") == (2, 2009)
assert check_range2("1188511880-1188511890") == (1, 1188511885)
assert check_range2("222220-222224") == (1, 222222)

assert check_list(test_data.strip().split(","), new=True) == (13, 4174379265)

answer_2 = check_list(ranges, new=True)
print(answer_2)
