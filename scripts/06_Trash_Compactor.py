## Day 6: Trash Compactor

from itertools import groupby
import math

# Part 1


test_data = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """


def parse_data(data):
    all_rows = data.strip().split("\n")
    rows = all_rows[:-1]
    operations = all_rows[-1].split()
    return [row.split() for row in rows], operations


assert parse_data(test_data) == (
    [
        ["123", "328", "51", "64"],
        ["45", "64", "387", "23"],
        ["6", "98", "215", "314"],
    ],
    ["*", "+", "*", "+"],
)


def apply_ops(nums, operations):
    total = 0
    for i in range(len(nums[0])):
        operation = operations[i]
        if operation == "*":
            result = 1
            for j in range(len(nums)):
                result *= int(nums[j][i])
        elif operation == "+":
            result = 0
            for j in range(len(nums)):
                result += int(nums[j][i])
        total += result
    return total


test_nums, test_ops = parse_data(test_data)
assert apply_ops(test_nums, test_ops) == 4277556


def complete_maths_homework(data):
    nums, ops = parse_data(data)
    return apply_ops(nums, ops)


with open("../input_data/06_Trash_Compactor.txt", "r", encoding="utf-8") as file:
    input_data = file.read()

answer_1 = complete_maths_homework(input_data)
print(answer_1)


# Part 2


def parse_data_ceph(data):
    all_rows = data.strip().split("\n")
    rows = all_rows[:-1]
    operations = all_rows[-1].split()[::-1]
    digits = [[row[0 + i : i + 1] for i in range(0, len(row))][::-1] for row in rows]
    nums = []
    for i in range(len(digits[0])):
        num = ""
        for j in range(len(digits)):
            num += digits[j][i]
        nums.append(num.strip())
    problems = (list(g) for k, g in groupby(nums, key="".__ne__) if k)
    return ([int(x) for x in problem] for problem in problems), operations


def apply_ops_ceph(problems, ops):
    total = 0
    for i, problem in enumerate(problems):
        if ops[i] == "*":
            result = math.prod(problem)
        elif ops[i] == "+":
            result = sum(problem)
        total += result
    return total


def complete_homework_ceph(data):
    problems, ops = parse_data_ceph(data)
    return apply_ops_ceph(problems, ops)


assert complete_homework_ceph(test_data) == 3263827


answer_2 = complete_homework_ceph(input_data)
print(answer_2)
