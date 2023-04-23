import json
import os
import re

from utparking.lib.map_parser import Parser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def main():
    with open(os.path.join(DATA_DIR, "sizes2.json"), "r") as f:
        sizes = json.load(f)
    p = Parser(os.path.join(DATA_DIR, "parsed.json"))

    to_remove = []
    for i, b in enumerate(p.buildings):
        if sizes["buildings"][b.name] == 0:
            to_remove.append(b.name)
    print(len(p.buildings))
    reduced = filter(lambda f: f.name not in to_remove, p.buildings)
    p.buildings = list(reduced)
    print(len(p.buildings))
    with open(os.path.join(DATA_DIR, "parsed2.json"), "w") as f:
        json.dump(p.to_json(), f, indent=4)


if __name__ == "__main__":
    main()
