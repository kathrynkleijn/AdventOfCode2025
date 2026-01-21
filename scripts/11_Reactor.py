# Day 11: Reactor

test_data = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

test_data2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


# Part 1


def parse_data(data):
    lines = data.split("\n")
    devices = {}
    for line in lines:
        key, connections = line.split(":")
        devices[key] = connections.split()
    return devices


assert parse_data(test_data.strip()) == {
    "aaa": ["you", "hhh"],
    "you": ["bbb", "ccc"],
    "bbb": ["ddd", "eee"],
    "ccc": ["ddd", "eee", "fff"],
    "ddd": ["ggg"],
    "eee": ["out"],
    "fff": ["out"],
    "ggg": ["out"],
    "hhh": ["ccc", "fff", "iii"],
    "iii": ["out"],
}


def out_path(devices, key="you", out=0):
    starters = devices[key]
    for starter in starters:
        next_devices = devices[starter]
        if "out" in next_devices:
            out += 1
        else:
            out = out_path(devices, key=starter, out=out)
    return out


test_devices = parse_data(test_data.strip())
assert out_path(test_devices) == 5


with open("../input_data/11_Reactor.txt", "r", encoding="utf-8") as file:
    input_data = file.read().strip()

answer_devices = parse_data(input_data)
answer_1 = out_path(answer_devices)
print(answer_1)


# Part 2


def out_path_svr(
    devices,
    in_key="svr",
    out=0,
    dac_flag=False,
    fft_flag=False,
    recursion_depth=0,
    level_dict=None,
):
    if level_dict is None:
        level_dict = {}

    starters = devices[in_key]
    if len(starters) > 1:
        for starter in starters:
            if starter not in level_dict:
                level_dict[starter] = recursion_depth
    for starter in starters:
        if starter in level_dict:
            recursion_depth = level_dict[starter]
            level_dict = {
                key: val for key, val in level_dict.items() if val <= recursion_depth
            }
            del level_dict[starter]
        if dac_flag and recursion_depth < dac_flag:
            dac_flag = False
        if fft_flag and recursion_depth < fft_flag:
            fft_flag = False

        if starter == "dac":
            dac_flag = recursion_depth
        elif starter == "fft":
            fft_flag = recursion_depth

        next_devices = devices[starter]
        if "out" in next_devices:
            if dac_flag and fft_flag:
                out += 1
        else:
            recursion_depth += 1
            out, dac_flag, fft_flag, recursion_depth, level_dict = out_path_svr(
                devices,
                in_key=starter,
                out=out,
                dac_flag=dac_flag,
                fft_flag=fft_flag,
                recursion_depth=recursion_depth,
                level_dict=level_dict,
            )

    return out, dac_flag, fft_flag, recursion_depth, level_dict


test_devices2 = parse_data(test_data2)
assert out_path_svr(test_devices2)[0] == 2

cache = {}


def x_to_y_path(devices, in_key, out_key, out=0):

    state = in_key
    out_in = out
    if state in cache:
        cached_out = cache[state]
        return out + cached_out

    starters = devices[in_key]
    for starter in starters:
        next_devices = devices[starter]
        if out_key in next_devices:
            out += 1
        elif "out" in next_devices:
            continue
        else:
            out = x_to_y_path(devices, in_key=starter, out_key=out_key, out=out)

    cache[state] = out - out_in
    return out


# print(x_to_y_path(test_devices2, "dac", "fft"))
# print(x_to_y_path(test_devices2, "fft", "dac"))
# print(x_to_y_path(test_devices2, "dac", "out"))


def svr_to_out_path(
    devices,
):
    svr_fft_paths = 0
    fft_out_paths = 0
    svr_dac_paths = 0
    dac_out_paths = 0

    cache.clear()
    dac_fft_paths = x_to_y_path(devices, "dac", "fft")
    cache.clear()
    fft_dac_paths = x_to_y_path(devices, "fft", "dac")
    cache.clear()

    if dac_fft_paths:
        svr_dac_paths = x_to_y_path(devices, "svr", "dac")
        cache.clear()
        fft_out_paths = x_to_y_path(devices, "fft", "out")
        cache.clear()
    if fft_dac_paths:
        svr_fft_paths = x_to_y_path(devices, "svr", "fft")
        cache.clear()
        dac_out_paths = x_to_y_path(devices, "dac", "out")
        cache.clear()

    return (
        svr_dac_paths * dac_fft_paths * fft_out_paths
        + svr_fft_paths * fft_dac_paths * dac_out_paths
    )


assert svr_to_out_path(test_devices2) == 2


answer_2 = svr_to_out_path(answer_devices)
print(answer_2)
