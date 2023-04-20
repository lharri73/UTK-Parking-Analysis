import json
import os
from csv import DictReader

from Levenshtein import distance

from utparking.lib.map_parser import Parser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def find_matching_building(read_buildings, building_name):
    try:
        return read_buildings[building_name]
    except KeyError:
        try:
            return read_buildings[building_name + " Building"]
        except KeyError:
            print("trying levenshtein")
            smallest = 10000
            smallest_idx = None
            for b in read_buildings.keys():
                cur = distance(building_name, b)
                if cur < smallest:
                    smallest = cur
                    smallest_idx = b
            print(f"Couldn't find {building_name} in BuildingList.csv")
            return read_buildings[smallest_idx] + "-LEVEN"

    return None


def main():
    with open(os.path.join(DATA_DIR, "bsizes.json"), "r") as f:
        bsizes = json.load(f)
    building_code_map = {}
    with open(os.path.join(DATA_DIR, "BuildingList.csv"), "r") as f:
        old_sizes = DictReader(f)
        for row in old_sizes:
            building_code_map.update({row["BUILDING NAME"]: row["REG CODE"]})
    p = Parser(os.path.join(DATA_DIR, "parsed.json"))

    for i, b in enumerate(p.buildings):
        code = find_matching_building(building_code_map, b.name)
        p.buildings[i].code = code

    to_dump = p.to_json()
    with open(os.path.join(DATA_DIR, "parsed2.json"), "w") as f:
        json.dump(to_dump, f, indent=4)


if __name__ == "__main__":
    main()
