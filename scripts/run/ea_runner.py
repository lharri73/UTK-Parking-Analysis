import os
import pickle

from utparking.lib.behavior_model import Runner
from utparking.lib.ea import EA

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def main():
    runner = Runner(DATA_DIR, time_scale=10)
    ea = EA(runner)
    means, maxs, fits, pops = ea.run()
    data = {"means": means, "maxs": maxs, "fits": fits, "pops": pops}

    with open("meta.pkl", "wb") as f:
        pickle.dump(data, f)


if __name__ == "__main__":
    main()
