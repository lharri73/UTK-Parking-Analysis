import os
import json

from utparking.lib.map_parser import Parser

data_file = os.path.join(os.path.dirname(__file__), '..', 'data')

def main():
    p  = Parser(os.path.join(data_file, 'tmp.json'))
    ret = {
        'parking': {b.name: 0 for b in p.parking},
        'buildings': {b.name: 0 for b in p.buildings}
    }
    with open(os.path.join(data_file, 'sizes.json'), 'w') as f:
        json.dump(ret, f, indent=4)

if __name__ == "__main__":
    main()