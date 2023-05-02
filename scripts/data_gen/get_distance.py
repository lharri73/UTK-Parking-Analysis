import json
# import googlemaps
import os

import numpy as np
from matplotlib import cm, colors
from matplotlib import pyplot as plt
from tqdm import tqdm

from utparking.lib.building import Building
from utparking.lib.map_parser import Parser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def generate_to_garages(p):
    origins = [dict(lat=35.960449, lng=-83.921852)]
    destinations = [b.to_request() for b in p.parking]
    # make requests for distance
    p.get_distance(origins, destinations, mode="driving")
    mat = p.gen_matrix(origins, destinations)
    np.save(os.path.join(DATA_DIR, "to_garages.npy"), mat)
    print(mat.shape)


def generate_btwn_garages(p):
    destinations = [b.to_request() for b in p.parking]
    origins = destinations
    # make requests for distance
    p.get_distance(origins, destinations, mode="driving")
    mat = p.gen_matrix(origins, destinations)
    np.save(os.path.join(DATA_DIR, "btwn_garages.npy"), mat)
    print(mat.shape)


def generate_to_buildings(p):
    origins = [b.to_request() for b in p.parking]
    destinations = [b.to_request() for b in p.buildings]
    # make requests for distance
    p.get_distance(origins, destinations, mode="walking")
    mat = p.gen_matrix(origins, destinations)
    np.save(os.path.join(DATA_DIR, "to_buildings.npy"), mat)
    print(mat.shape)


def main():
    p = Parser(os.path.join(DATA_DIR, "parsed.json"))
    generate_to_garages(p)
    generate_btwn_garages(p)
    generate_to_buildings(p)

    # buildings, parking = p.construct_requests()
    # origins = origins[:10]
    # destinations = destinations[:10]
    # matrix = p.get_distance(origins, destinations)
    # matrix = p.gen_matrix()
    # matrix /= 60
    #
    # mean_buildings = np.nanmean(matrix[0, :, :], axis=1)
    # mean_parking = np.nanmean(matrix[0, :, :], axis=0)
    #
    # ## order the matrix so it's easy to read
    # sorted_buildings = np.flip(np.argsort(mean_buildings))
    # sorted_parking = np.flip(np.argsort(mean_parking))
    # matrix = matrix[:, sorted_buildings, :][:, :, sorted_parking]
    #
    # building_names_sorted = [p.buildings[i].name for i in sorted_buildings]
    # parking_names_sorted = [p.parking[i].name for i in sorted_parking]
    #
    # fig = plt.figure(figsize=(15, 30))
    # plt.imshow(matrix[1, :, :])
    # plt.xticks(np.arange(len(parking)), parking_names_sorted, rotation=90)
    # plt.yticks(np.arange(len(buildings)), building_names_sorted)
    #
    # # define color map
    # cmap = cm.get_cmap("viridis")
    # norm = colors.Normalize(np.min(matrix), np.max(matrix))
    # # plot colorbar
    # plt.colorbar(
    #     cm.ScalarMappable(norm=norm, cmap=cmap), ax=plt.gca(), fraction=0.05, aspect=50
    # )
    # plt.savefig("matrix.pdf")
    # print("done")


if __name__ == "__main__":
    main()
