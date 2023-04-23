import copy
import csv
import json
import os
import re
from collections import OrderedDict

from utparking.lib.map_parser import Parser

data_file = os.path.join(os.path.dirname(__file__), "..", "data")


def main():
    p = Parser(os.path.join(data_file, "parsed.json"))
    with open(os.path.join(data_file, "sizes.json"), "r") as f:
        cur_sizes = json.load(f)

    with open(os.path.join(data_file, "bsizes.json"), "r") as f:
        bsizes = json.load(f)

    allCodes = OrderedDict({b.code: 0 for b in p.buildings})
    sizes = bsizes["rows"]
    code_pattern = re.compile(r"[A-Z0-9]+")
    for room in sizes:
        info = room["row"]
        room_name = info[1]["itemName"]
        building_code = re.search(code_pattern, room_name)
        cur_code = building_code.group(0)
        cur_size = int(info[6])
        if cur_size >= 500:
            ## ignore super large classrooms/outdoor areas
            continue
        try:
            allCodes[cur_code] += cur_size
        except KeyError:
            pass

    buildings_sizes = {}
    for b in p.buildings:
        try:
            buildings_sizes.update({b.name: allCodes[b.code]})
        except KeyError as e:
            print(e)
            continue

    ret = {
        "parking": cur_sizes["parking"],
        "buildings": buildings_sizes,
    }

    with open(os.path.join(data_file, "sizes2.json"), "w") as f:
        json.dump(ret, f, indent=4)


if __name__ == "__main__":
    main()
