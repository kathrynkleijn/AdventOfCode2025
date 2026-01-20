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


def out_path_svr(devices, key="svr", out=0, dac_flag=False, fft_flag=False):
    starters = devices[key]
    for starter in starters:
        print(f"{starter=}")
        if starter == "dac":
            dac_flag = True
        elif starter == "fft":
            fft_flag = True
        next_devices = devices[starter]
        if "out" in next_devices:
            if dac_flag and fft_flag:
                out += 1
                print("out", True)
            print("out")
            # only reset if returning to server - need to keep track of "layers"
            dac_flag = False
            fft_flag = False

        else:
            out, dac_flag, fft_flag = out_path_svr(
                devices, key=starter, out=out, dac_flag=dac_flag, fft_flag=fft_flag
            )
    return out, dac_flag, fft_flag


test_devices2 = parse_data(test_data2)
print(out_path_svr(test_devices2))
