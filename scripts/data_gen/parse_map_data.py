import json
import os

from utparking.lib.map_parser import Parser

data_file = os.path.join(os.path.dirname(__file__), '..', 'data')


def main():
    p = Parser(os.path.join(data_file, 'response2.json'))
    with open(os.path.join(data_file, 'parsed3.json'), 'w') as f:
        json.dump(p.to_json(), f, indent=4)


if __name__ == "__main__":
    main()
