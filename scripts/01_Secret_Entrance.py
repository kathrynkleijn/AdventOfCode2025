test_data = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

test_result = 3
start_num = 0


def parse_rotations(data):
    rotation_list = []
    for item in data:
        if item[0] == "R":
            rotation_list.append(int(item[1:]))
        elif item[0] == "L":
            rotation_list.append(-int(item[1:]))
    return rotation_list


assert parse_rotations(test_data.strip().split("\n")) == [
    -68,
    -30,
    48,
    -5,
    60,
    -55,
    -1,
    -99,
    14,
    -82,
]


def rotate(rotation_list, start_num=50, dial_max=99):
    current = start_num
    password = 0
    for item in rotation_list:
        current = (current + item) % (dial_max + 1)
        if current == 0:
            password += 1
    return password


test_list = [
    -68,
    -30,
    48,
    -5,
    60,
    -55,
    -1,
    -99,
    14,
    -82,
]

assert rotate(test_list) == 3


with open("../input_data/01_Secret_Entrance.txt", "r", encoding="utf-8") as file:
    data = file.read().strip().split("\n")

rotation_list1 = parse_rotations(data)
answer_1 = rotate(rotation_list1)
print(answer_1)
