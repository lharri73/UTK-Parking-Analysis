import os
import json
import re

from utparking.lib.map_parser import Parser


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def main():
    with open(os.path.join(DATA_DIR, 'bsizes.json'), 'r') as f:
        sizes = json.load(f)
    p = Parser(os.path.join(DATA_DIR, 'parsed2.json'))
    codes = [b.code for b in p.buildings]
    capacities = [0]*len(codes)

    sizes = sizes['rows']
    code_pattern = re.compile(r'[A-Z0-9]+')
    not_found = set()
    for room in sizes:
        info = room['row']
        room_name = info[1]['itemName']
        building_code = re.search(code_pattern, room_name)
        cur_code = building_code.group(0)
        if cur_code not in codes:
            not_found.add(cur_code)
        else:
            idx = codes.index(cur_code)
            capacities[idx] += info[6]
        
    print(f"Could not find the following buildings in the building list: {not_found}")
    print(capacities)
    new_cap = filter(lambda x: x == 0, capacities)
    print(len(list(new_cap)))

if __name__ == "__main__":
    main()
