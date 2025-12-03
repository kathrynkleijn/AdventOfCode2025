## Day 3: Lobby

# Part 1

test_data = """987654321111111
811111111111119
234234234234278
818181911112111"""


def find_maximum_battery(batteries):
    max_size = max(batteries)
    return max_size, [i for i, b in enumerate(batteries) if b == max_size]


def find_bank_joltage(batteries):
    max_size, indices = find_maximum_battery(batteries)
    if len(indices) > 1:
        second_size = max_size
    elif indices[0] == len(batteries) - 1:
        second_size = max_size
        batteries = batteries[:-1]
        max_size, inidices = find_maximum_battery(batteries)
    else:
        batteries = batteries[indices[0] + 1 :]
        second_size, second_indices = find_maximum_battery(batteries)
    joltage = str(max_size) + str(second_size)
    return int(joltage)


def total_joltage(banks):
    joltage = 0
    for bank in banks:
        batteries = [int(b) for b in list(bank)]
        joltage += find_bank_joltage(batteries)
    return joltage


assert total_joltage(["987654321111111"]) == 98
assert total_joltage(["811111111111119"]) == 89

assert total_joltage(test_data.strip().split("\n")) == 357

with open("../input_data/03_Lobby.txt", "r", encoding="utf-8") as file:
    answer_banks = file.read().strip().split("\n")

answer_1 = total_joltage(answer_banks)
print(answer_1)


# Part 2


def find_next_battery(batteries, battery_num):
    num_batteries = len(batteries)
    num_remaining = 13 - battery_num
    largest_index = num_batteries - num_remaining
    max_size = max(batteries[: largest_index + 1])
    return max_size, batteries.index(max_size)


test_bat1 = [int(b) for b in list("987654321111111")]
test_bat2 = [int(b) for b in list("234234234234278")]
assert find_next_battery(test_bat1, 1) == (9, 0)
assert find_next_battery(test_bat2, 1) == (4, 2)


def find_bank_joltage_12(batteries):
    joltage = ""
    for i in range(1, 13):
        size, index = find_next_battery(batteries, i)
        joltage += str(size)
        batteries = batteries[index + 1 :]
        if len(batteries) == (12 - i):
            remaining_batteries = "".join(str(b) for b in batteries)
            joltage += remaining_batteries
            break
    return int(joltage)


assert find_bank_joltage_12(test_bat1) == 987654321111
assert find_bank_joltage_12(test_bat2) == 434234234278


def total_joltage_12(banks):
    joltage = 0
    for bank in banks:
        batteries = [int(b) for b in list(bank)]
        joltage += find_bank_joltage_12(batteries)
    return joltage


assert total_joltage_12(test_data.strip().split("\n")) == 3121910778619

answer_2 = total_joltage_12(answer_banks)
print(answer_2)
