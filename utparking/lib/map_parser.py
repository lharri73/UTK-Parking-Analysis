import json
from utparking.lib.building import Building
import numpy as np
from tqdm import tqdm
import os
import googlemaps
class Parser:
    def __init__(self, data_file='utparking/data/tmp.json'):
        with open(data_file, 'r') as f:
            data = json.load(f)
        if isinstance(data, list):
            self.buildings = Building.parse_buildings(data)
            self.parking = Building.parse_parking(data)
        elif isinstance(data, dict):
            ## parsed already
            self.buildings = [Building(b['name'], b['lat'], b['lon'], b['cat']) for b in data['buildings']]
            self.parking = [Building(b['name'], b['lat'], b['lon'], b['cat']) for b in data['parking']]
        self.client = googlemaps.Client(os.environ.get('MAPS_API_KEY', 'INVALID_KEY-CHANGE_ME'))
        self.results_folder = "utparking/data/results"
        self.results_counter = 0
        self.distance_matrix = np.empty((2, len(self.buildings), len(self.parking)))

        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)

    def construct_requests(self):
        origins = [dict(lat=b.lat,lng=b.lon) for b in self.buildings]
        destinations = [dict(lat=b.lat,lng=b.lon) for b in self.parking]
        return origins, destinations

    def get_distance(self, origin, destination):
        num_items = 10
        chunks_origin = [origin[i:min(i+num_items,len(origin))] for i in range(0, len(origin), num_items)]
        dest_origin = [destination[i:min(i+num_items,len(destination))] for i in range(0, len(destination), num_items)]
        for i, chunk in tqdm(enumerate(chunks_origin), position=1):
            for j, dest in tqdm(enumerate(dest_origin)):
                result = self.client.distance_matrix(chunk, dest, mode='walking')
                with open(f"{self.results_folder}/{self.results_counter}.json", 'w') as f:
                    json.dump(result, f, indent=4)
                self.results_counter += 1
                # self.distance_matrix[i,j] = result
        # result = self.client.distance_matrix(origin, destination, mode='walking')
        # with open(f"{self.results_folder}/{self.results_counter}.json", 'w') as f:
        #     json.dump(result, f, indent=4)
        # return result

    def gen_matrix(self):
        origin, destination = self.construct_requests()
        num_items = 10
        chunks_origin = [origin[i:min(i+num_items,len(origin))] for i in range(0, len(origin), num_items)]
        dest_origin = [destination[i:min(i+num_items,len(destination))] for i in range(0, len(destination), num_items)]
        matrix = np.empty((2, len(origin), len(destination)))

        for i, chunk in enumerate(chunks_origin):
            for j, dest in enumerate(dest_origin):

                with open(f"{self.results_folder}/{self.results_counter}.json", 'r') as f:
                    result = json.load(f)
                self.results_counter += 1

                for k, row in enumerate(result['rows']):
                    for l, element in enumerate(row['elements']):
                        if element['status'] == 'OK':
                            matrix[0,i*num_items+k,j*num_items+l] = element['distance']['value']
                            matrix[1, i * num_items + k, j * num_items + l] = element['duration']['value']
                        else:
                            matrix[:, i * num_items + k, j * num_items + l] = np.nan
        return matrix

    def to_json(self):
        return {
            'buildings': [b.to_json() for b in self.buildings],
            'parking': [b.to_json() for b in self.parking]
        }