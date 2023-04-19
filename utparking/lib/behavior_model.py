import json
import os
from enum import Enum, IntEnum, auto

import numpy as np


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

    def find_closest_garage(self, metric=TravelMetric.time):
        assert self.dest_idx < self.runner.to_b.shape[2], "Invalid destination idx"
        closest_garage = np.argmin(self.runner.to_b[metric, :, self.dest_idx])
        return closest_garage

    def tick(self):
        pass


class Runner:
    def __init__(self, data_dir):
        """
        :param data_dir(str): directory containing processed matrices and
                              sizes of buildings/parking lots

        to_g (2,1,garages): (Distance,time) from origin to each garage
        to_b (2,garages,buildings): (Distance,time) from garages to each garage
        btwn_g: (2,garages,garage): (Distance,time) from each garage to each other garage
        """
        self.to_b = np.load(os.path.join(data_dir, "to_buildings.npy"))
        self.to_g = np.load(os.path.join(data_dir, "to_garages.npy"))
        self.btwn_g = np.load(os.path.join(data_dir, "btwn_garages.npy"))
        with open(os.path.join(data_dir, "sizes.json")) as f:
            self.sizes = json.load(f)


def test_func():
    ## I only put this shit in a function to make sure I don't have scoping problems while testing
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    runner = Runner(DATA_DIR)


if __name__ == "__main__":
    test_func()
