import json
from functools import reduce
# import googlemaps
import os
import numpy as np
from tqdm import tqdm

from matplotlib import pyplot as plt
from matplotlib import cm, colors


class Building:
    def __init__(self, name, lat, lon, cat):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.cat = cat

    def __str__(self):
        return f"<Building: '{self.name}' at ({self.lat}, {self.lon})>"

    def __eq__(self, other):
        return self.name == other.name


def parse_buildings(data):
    academic_buildings = data[80]['children']['locations']
    buildings = map(lambda x: Building(x['name'], x['lat'], x['lng'], x['catId']), academic_buildings)

    return list(buildings)

    # 80: academic and administrative
    # 66: Commuter
    # 67: Non-Commuter
    # 73: Perimeter Commuter
    # 74: Perimeter Non-Commuter

def parse_parking(data):
    commuter_data = data[66]['children']['locations']
    commuter = [Building(x['name'], x['lat'], x['lng'], x['catId']) for x in commuter_data]
    non_commuter_data = data[67]['children']['locations']
    non_commuter = [Building(x['name'], x['lat'], x['lng'], x['catId']) for x in non_commuter_data]
    perim_commuter_data = data[73]['children']['locations']
    perim_commuter = [Building(x['name'], x['lat'], x['lng'], x['catId']) for x in perim_commuter_data]
    perim_non_commuter_data = data[74]['children']['locations']
    perim_non_commuter = [Building(x['name'], x['lat'], x['lng'], x['catId']) for x in perim_non_commuter_data]

    full = commuter + non_commuter + perim_commuter + perim_non_commuter
    parking = unique(full)
    return parking

def unique(list1):
    # Print directly by using * symbol
    ans = reduce(lambda re, x: re + [x] if x not in re else re, list1, [])
    return ans


class Parser:
    def __init__(self):
        with open('tmp.json', 'r') as f:
            data = json.load(f)
        self.buildings = parse_buildings(data)
        self.parking = parse_parking(data)
        # self.client = googlemaps.Client(os.environ['MAPS_API_KEY'])
        self.results_folder = "results"
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
                # with open()
                with open(f"{self.results_folder}/{self.results_counter}.json", 'w') as f:
                    json.dump(result, f, indent=4)
                self.results_counter += 1
                # self.distance_matrix[i,j] = result
        # result = self.client.distance_matrix(origin, destination, mode='walking')
        # with open(f"{self.results_folder}/{self.results_counter}.json", 'w') as f:
        #     json.dump(result, f, indent=4)
        # return result

    def gen_matrix(self, origin, destination):
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


def main():
    p = Parser()

    buildings, parking = p.construct_requests()
    # origins = origins[:10]
    # destinations = destinations[:10]
    # matrix = p.get_distance(origins, destinations)
    matrix = p.gen_matrix(buildings, parking)
    matrix /= 60

    mean_buildings = np.nanmean(matrix[0,:,:], axis=1)
    mean_parking = np.nanmean(matrix[0,:,:], axis=0)

    sorted_buildings = np.flip(np.argsort(mean_buildings))
    sorted_parking = np.flip(np.argsort(mean_parking))
    matrix = matrix[:,sorted_buildings,:][:,:,sorted_parking]

    building_names_sorted = [p.buildings[i].name for i in sorted_buildings]
    parking_names_sorted = [p.parking[i].name for i in sorted_parking]

    fig = plt.figure(figsize=(15, 30))
    plt.imshow(matrix[1,:,:])
    plt.xticks(np.arange(len(parking)), parking_names_sorted, rotation=90)
    plt.yticks(np.arange(len(buildings)), building_names_sorted)

    # define color map
    cmap = cm.get_cmap("viridis")
    norm = colors.Normalize(np.min(matrix), np.max(matrix))
    # plot colorbar
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), fraction=0.05, aspect=50)
    plt.text(0.5, 0.5, 'DRAFT', transform=plt.gca().transAxes,
            fontsize=300, color='gray', alpha=0.5,
            ha='center', va='center', rotation=70)
    plt.savefig('matrix.pdf')
    print("done")


if __name__ == "__main__":
    main()
