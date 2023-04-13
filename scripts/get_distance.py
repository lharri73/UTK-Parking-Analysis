import json

# import googlemaps
import os
import numpy as np
from tqdm import tqdm

from matplotlib import pyplot as plt
from matplotlib import cm, colors

from utparking.lib.building import Building
from utparking.lib.map_parser import Parser


def main():
    p = Parser()

    # buildings, parking = p.construct_requests()
    # origins = origins[:10]
    # destinations = destinations[:10]
    # matrix = p.get_distance(origins, destinations)
    matrix = p.gen_matrix()
    matrix /= 60

    mean_buildings = np.nanmean(matrix[0,:,:], axis=1)
    mean_parking = np.nanmean(matrix[0,:,:], axis=0)

    ## order the matrix so it's easy to read
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
    plt.savefig('matrix.pdf')
    print("done")


if __name__ == "__main__":
    main()
