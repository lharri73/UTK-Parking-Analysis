import multiprocessing
import os
import pickle
import random

from utparking.lib.behavior_model import Runner

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def run_func(seed):
    random.seed(seed)
    runner = Runner(DATA_DIR, time_scale=10)
    runner.setup_run()
    num_checked, time_parking = runner.run()

    return num_checked, time_parking


def main():
    nums = [random.randint(0, 20480) for _ in range(10)]
    with multiprocessing.Pool(10) as p:
        ret = p.map(run_func, nums)
    # ret = list(map(run_func, nums))

    with open("multirun.pkl", "wb") as f:
        pickle.dump(ret, f)


if __name__ == "__main__":
    main()
