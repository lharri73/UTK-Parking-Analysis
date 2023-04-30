import json
import os
import random
import time as pytime
from enum import Enum, IntEnum, auto
from functools import reduce
from operator import add

import numpy as np

from utparking.lib.log import get_logger
from utparking.lib.map_parser import Parser
from utparking.lib.time_utils import Ticker


class State(Enum):
    initial_search = auto()
    traveling = auto()
    searching = auto()
    parking = auto()
    parked = auto()
    stuck = auto()


class TravelMetric(IntEnum):
    distance = 0
    time = 1

class Policy(Enum):
    random = 0
    closest = 1
    largest = 2
    smallest = 3

cur_idx = 0
GLOBAL_TIME = Ticker()


class Parking:
    def __init__(self, name, capacity, searching_rate=3.3):
        self.name = name
        self.capacity = capacity
        self.searching = []
        self.parked = []
        self.search_time = self.capacity / searching_rate

    def add_student(self, idx, agressive):
        time_to_comp = self.search_time * (len(self.parked) / self.capacity) * agressive
        done_time = GLOBAL_TIME() + time_to_comp
        item = [idx, done_time]
        self.searching.append(item)

    def check(self, idx):
        """
        Check to see if it found parking, if it's still searching,
        or if it exited and didn't find anything

        ret 0: still waiting,
            1: found parking,
            2: didn't find parking
        """
        assert (
            len(self.searching) > 0
        ), "Trying to check status when there are no students parking"

        # The one checking is not the first in line
        if self.searching[0][0] != idx:
            return 0

        # Check to see if done waiting
        cur_time = GLOBAL_TIME()
        if cur_time >= self.searching[0][1]:
            diff_check(cur_time, self.searching[0][1])
            self.searching.pop(0)
            if len(self.parked) >= self.capacity:
                # the parking lot is full
                return 2
            else:
                # not full, searched until we found a spot, parked
                self.parked.append(idx)
                return 1
        else:
            return 0


class Student:
    agressive: float  # how quickly do they thrash through the parking lots (<1 is more aggressive, >1 is grandma)
    park_duration: float  # how long in minutes are they going to stay parked (5-480)
    speed_adj: float  # multiplier to the driving time
    prob_retry_lot: float  # probability that the student will retry a lot they have already looked for a spot in
    dest_idx: int  # idx of the building the student is trying to get to

    def __init__(self, runner, dest_idx, global_speed_adj=1.0, genome=None):
        """
        :param runner: reference to the runner object
        """
        global cur_idx
        self.id = cur_idx
        cur_idx += 1
        self.runner = runner
        self.garages_tried = []
        self.dest_idx = dest_idx
        self.state = State.initial_search

        if genome is None:
            self.speed_adj = (random.randrange(128 + 64, 256) / 256.0) * global_speed_adj
            self.agressive = random.randrange(128, 256 + 128) / 256.0
            self.policy = Policy.closest
        else:
            genome = np.packbits(genome)[0]
            self.speed_adj = (((genome & 0xff) / 256.0)+0.5) * global_speed_adj # 0.5-1.5
            self.agressive = ((2*(genome >> 8)) / 256.0)  # 0-2
            self.policy = Policy((genome >> 16) & 0x3)

        # internal params
        self.going_to = None
        self.wait_until = None
        self.parked_searched = []

    def find_closest_garage(self, metric=TravelMetric.time):
        assert self.dest_idx < self.runner.to_b.shape[2], "Invalid destination idx"
        closest_garage = np.argmin(self.runner.to_b[metric, :, self.dest_idx])
        return closest_garage

    def __update_wait_until(self):
        travel_time = self.runner.to_b[
            self.runner.dist_met, self.going_to, self.dest_idx
        ]
        travel_time *= self.speed_adj
        self.wait_until = GLOBAL_TIME() + travel_time

        self.state = State.traveling     

    def tick(self):
        if self.state == State.initial_search:
            # Find where we need to go and how long it will take to get there
            if self.policy == Policy.closest:
                self.going_to = np.argmin(
                    self.runner.to_b[self.runner.dist_met, :, self.dest_idx]
                )
            elif self.policy == Policy.random:
                self.going_to = random.randrange(self.runner.to_b.shape[1])
            elif self.policy == Policy.largest:
                self.going_to = np.argmax(
                    self.runner.sizes["parking"].values()
                )
            elif self.policy == Policy.smallest:
                self.going_to = np.argmin(
                    self.runner.sizes["parking"].values()
                )
            else:
                raise ValueError(f"Unknown policy {self.policy}")

            self.__update_wait_until()

        elif self.state == State.traveling:
            # The student is traveling from the interstate to the parking area
            assert (
                self.wait_until is not None
            ), "did not set a time to wait until. This student will wait forever <dun dun dunnn>"
            if GLOBAL_TIME() >= self.wait_until:
                diff_check(GLOBAL_TIME(), self.wait_until)
                self.state = State.parking
                self.wait_until = None
                self.runner.parking[self.going_to].add_student(self.id, self.agressive)
        elif self.state == State.parking:
            check_stat = self.runner.parking[self.going_to].check(self.id)
            if check_stat == 0:
                # still waiting
                pass
            elif check_stat == 1:
                # Found parking
                self.state = State.parked
            elif check_stat == 2:
                # didn't find parking
                self.parked_searched.append(self.going_to)
                self.state = State.searching
        elif self.state == State.searching:
            if self.policy == Policy.closest:
                closest = np.argsort(
                    self.runner.btwn_g[self.runner.dist_met, self.going_to, :]
                )
                for idx in closest:
                    if idx in self.parked_searched:
                        continue
                    self.going_to = idx
                    break
                else:
                    self.state = State.stuck
            elif self.policy == Policy.largest:
                largest = np.argsort(self.runner.sizes["parking"].values(), reverse=True)
                for idx in largest:
                    if idx in self.parked_searched:
                        continue
                    self.going_to = idx
                    break
                else:
                    self.state = State.stuck
            elif self.policy == Policy.smallest:
                smallest = np.argsort(self.runner.sizes["parking"].values())
                for idx in smallest:
                    if idx in self.parked_searched:
                        continue
                    self.going_to = idx
                    break
                else:
                    self.state = State.stuck
            elif self.policy == Policy.random:
                possible = np.array(list(range(len(self.runner.sizes["parking"]))))
                np.random.shuffle(possible)
                for idx in possible:
                    if idx in self.parked_searched:
                        continue
                    self.going_to = idx
                    break
                else:
                    self.state = State.stuck
            else:
                raise ValueError(f"Unknown policy {self.policy}")

            self.__update_wait_until()

        elif self.state == State.parked:
            # Do nothing...for now, do we make them eventually move?
            return
        elif self.state == State.stuck:
            print(f"student {self.id} going to {self.dest_idx} tried {len(self.garages_tried)} locations and is stuck")
            return
        else:
            raise ValueError(f"Unknown state for student {self.id}")
    

    def __str__(self):
        return f"<Student {self.id} who is {self.state} going to {self.dest_idx}>"

    def __repr__(self):
        return str(self)
    
    def fitness(self):
        if self.state == State.parked:
            travel_time = self.runner.to_b[self.runner.dist_met, self.going_to, self.dest_idx]
            max_time = np.max(self.runner.to_b[self.runner.dist_met, :, self.dest_idx])
            f = travel_time / max_time
            return f
        else:
            return 0


class Runner:
    def __init__(self, data_dir, vehicle_occupancy=1.5, time_scale=1.0):
        """
        :param data_dir(str): directory containing processed matrices and
                              sizes of buildings/parking lots
        :param vehicle_occupancy(float): Average number of people per vehicle

        to_g (2,1,garages): (Distance,time) from origin to each garage
        to_b (2,garages,buildings): (Distance,time) from garages to each garage
        btwn_g: (2,garages,garage): (Distance,time) from each garage to each other garage
        """
        self.dist_met = TravelMetric.time
        self.log = get_logger()

        self.log.debug(f"Reading matrices from {data_dir}")
        self.to_b = np.load(os.path.join(data_dir, "to_buildings.npy"))
        self.to_g = np.load(os.path.join(data_dir, "to_garages.npy"))
        self.btwn_g = np.load(os.path.join(data_dir, "btwn_garages.npy"))
        self.time_scale = time_scale

        sizes_path = os.path.join(data_dir, "sizes.json")
        self.log.debug(f"Reading sizes from {sizes_path}")
        with open(sizes_path) as f:
            self.sizes = json.load(f)

        self.max_occ = reduce(add, self.sizes["buildings"].values(), 0)
        parking_limit = (
            reduce(add, self.sizes["parking"].values(), 0) * vehicle_occupancy
        )
        self.parser = Parser(os.path.join(data_dir, "parsed.json"))
        self.log.debug(
            f"Found {len(self.parser.buildings)} buildings with {self.max_occ} occuancy limit"
        )
        self.max_parks = int(parking_limit/vehicle_occupancy)
        self.log.debug(
            f"Found {len(self.parser.parking)} parking areas with {self.max_parks} spaces"
        )
        
        self.log.info("Runner initialization complete")
        

    def setup_run(self, student_genomes=None):
        self.log.debug("Creating students")
        self.students = []
        i=0
        for b_name, b_cap in self.sizes["buildings"].items():
            for _ in range(b_cap):
                d_idx = self.parser.buildings.index(b_name)
                self.students.append(
                    Student(self, d_idx, global_speed_adj=1 / self.time_scale, genome=student_genomes[i])
                )
                i += 1
        self.log.info(f"Created {len(self.students)} student objects")
        self.log.debug(f"Creaint Parking Areas")
        self.parking = []
        for i, (p_name, p_cap) in enumerate(self.sizes["parking"].items()):
            assert p_name == self.parser.parking[i].name, "name mismatch"
            self.parking.append(Parking(p_name, p_cap, 3.3 * self.time_scale))
        self.log.info(f"Created {len(self.parking)} parking objects")

    def num_students(self):
        s = reduce(add, self.sizes["buildings"].values(), 0)
        return s
    
    def reset(self):
        GLOBAL_TIME.reset()
        self.students = []
        self.parking = []


    def print_stats(self):
        stats = {data: 0 for data in State}
        for student in self.students:
            stats[student.state] += 1
        print(stats)
        return stats

    def run(self):
        print("start")
        i = -1
        tim = 0
        while True:
            i += 1
            tic = pytime.time()
            for student in self.students:
                student.tick()
            toc = pytime.time()
            tim = tim * 0.99 + (toc - tic) * 0.01

            if i % 100 == 0:
                stats = self.print_stats()
                print(f"avg process time: {tim:0.4f}s")
                if stats[State.parked] == self.max_parks:
                    break
            GLOBAL_TIME.tick()

        fitnesses = [s.fitness() for s in self.students]
        return fitnesses

def diff_check(cur_time, stop_time):
    if stop_time - cur_time > 5:
        print("found large diff")

def test_func():
    ## I only put this shit in a function to make sure I don't have scoping problems while testing
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    runner = Runner(DATA_DIR)


if __name__ == "__main__":
    test_func()
