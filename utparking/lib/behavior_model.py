import json
import os
from enum import Enum, IntEnum, auto
from functools import reduce
from operator import add

import numpy as np

from utparking.lib.log import get_logger


class State(Enum):
    initial_search = auto()
    searching = auto()
    parking = auto()
    parked = auto()


class TravelMetric(IntEnum):
    distance = 0
    time = 1


class Student:
    agressive: float  # how quickly do they thrash through the parking lots
    park_duration: float  # how long in minutes are they going to stay parked (5-480)
    speed_adj: float  # multiplier to the driving speed
    prob_retry_lot: float  # probability that the student will retry a lot they have already looked for a spot in
    dest_idx: int  # idx of the building the student is trying to get to

    def __init__(self, runner):
        """
        :param runner: reference to the runner object
        """
        self.runner = runner
        self.garages_tried = []

    def find_closest_garage(self, metric=TravelMetric.time):
        assert self.dest_idx < self.runner.to_b.shape[2], "Invalid destination idx"
        closest_garage = np.argmin(self.runner.to_b[metric, :, self.dest_idx])
        return closest_garage

    def tick(self):
        pass


class Runner:
    def __init__(self, data_dir, space_per_student=30):
        """
        :param data_dir(str): directory containing processed matrices and
                              sizes of buildings/parking lots

        to_g (2,1,garages): (Distance,time) from origin to each garage
        to_b (2,garages,buildings): (Distance,time) from garages to each garage
        btwn_g: (2,garages,garage): (Distance,time) from each garage to each other garage
        """
        self.log = get_logger()

        self.log.debug(f"Reading matrices from {data_dir}")
        self.to_b = np.load(os.path.join(data_dir, "to_buildings.npy"))
        self.to_g = np.load(os.path.join(data_dir, "to_garages.npy"))
        self.btwn_g = np.load(os.path.join(data_dir, "btwn_garages.npy"))

        sizes_path = os.path.join(data_dir, "sizes.json")
        self.log.debug(f"Reading sizes from {sizes_path}")
        with open(sizes_path) as f:
            self.sizes = json.load(f)

        self.garages = [dict(parked=[], parking=[])] * self.to_g.shape[1]

        max_occupancy = reduce(add, self.sizes["buildings"].values(), 0)
        num_students = max_occupancy // space_per_student
        print(num_students)

        self.log.info("Runner initialization complete")

    def run(self):
        pass


def test_func():
    ## I only put this shit in a function to make sure I don't have scoping problems while testing
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    runner = Runner(DATA_DIR)


if __name__ == "__main__":
    test_func()
