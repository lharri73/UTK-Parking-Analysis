from enum import Enum, auto

import numpy as np


class State(Enum):
    searching = auto()
    parking = auto()
    parked = auto()


class Student:
    agressive: float  # how quickly do they thrash through the parking lots
    park_duration: float  # how long in minutes are they going to stay parked (5-480)
    speed_adj: float  # multiplier to the driving speed
    prob_retry_lot: float  # probability that the student will retry a lot they have already looked for a spot in
    dest_idx: int  # idx of the building the student is trying to get to

    def __init__(self):
        pass


class Runner:
    pass
