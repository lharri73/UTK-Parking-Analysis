import os
import json
import csv
import copy

from utparking.lib.map_parser import Parser

data_file = os.path.join(os.path.dirname(__file__), '..', 'data')

def main():
    p  = Parser(os.path.join(data_file, 'tmp.json'))
    ret = {
        'parking': {b.name: 0 for b in p.parking},
        'buildings': {b.name: 0 for b in p.buildings}
    }

    read_buildings = {}
    with open(os.path.join(data_file, 'BuildingList.csv'), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            read_buildings[row['BUILDING NAME']] = float(row['NET RM SQFT'])

    for b in p.buildings:
        try:
            ret['buildings'][b.name] = read_buildings[b.name]
        except KeyError:
            try:
                ret['buildings'][b.name] = read_buildings[b.name + " Building"]
            except KeyError:
                pass
            print(f"Couldn't find {b.name} in BuildingList.csv")
            continue

    with open(os.path.join(data_file, 'sizes.json'), 'w') as f:
        json.dump(ret, f, indent=4)

if __name__ == "__main__":
    main()