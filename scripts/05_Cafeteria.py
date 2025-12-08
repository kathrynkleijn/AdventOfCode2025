## Day 5: Cafeteria

# Part 1

test_data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


def parse_data(data):
    ranges = data.split("\n\n")[0].split("\n")
    ids = data.split("\n\n")[1].split("\n")
    return ranges, ids


assert parse_data(test_data) == (
    ["3-5", "10-14", "16-20", "12-18"],
    [
        "1",
        "5",
        "8",
        "11",
        "17",
        "32",
    ],
)


def fresh_ids(ranges):
    fresh = []
    for id_range in ranges:
        start = id_range.split("-")[0]
        stop = id_range.split("-")[1]
        fresh.append([int(start), int(stop)])
    return (id_range for id_range in sorted(fresh))


test_ranges, test_ids = parse_data(test_data)
assert [x for x in fresh_ids(test_ranges)] == [[3, 5], [10, 14], [12, 18], [16, 20]]


# def sort_fresh_ids(ranges):
#     fresh = []
#     for id_range in fresh_ids(ranges):
#         updated = False
#         for num, fresh_range in enumerate(fresh):
#             if (
#                 fresh_range[0] <= id_range[0] <= fresh_range[1]
#                 and id_range[1] > fresh_range[1]
#             ):
#                 fresh[num] = [fresh_range[0], id_range[1]]
#                 updated = True
#             elif (
#                 id_range[0] < fresh_range[0]
#                 and fresh_range[0] <= id_range[1] <= fresh_range[1]
#             ):
#                 fresh[num] = [id_range[0], fresh_range[1]]
#                 updated = True
#             elif id_range[0] < fresh_range[0] and id_range[1] > fresh_range[1]:
#                 fresh[num] = id_range
#                 updated = True
#         if not updated:
#             fresh.append(id_range)
#     return (id_range for id_range in sorted(fresh))


# assert [x for x in sort_fresh_ids(test_ranges)] == [[3, 5], [10, 20]]


def is_it_fresh(id, fresh_range):
    return True if fresh_range[0] <= id <= fresh_range[1] else False


def count_fresh(data):
    count = 0
    ranges, ids = parse_data(data)
    for id in ids:
        for fresh_range in fresh_ids(ranges):
            if is_it_fresh(int(id), fresh_range):
                count += 1
                break
    return count


assert count_fresh(test_data) == 3

with open("../input_data/05_Cafeteria.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_1 = count_fresh(input_data)
print(answer_1)
