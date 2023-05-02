import multiprocessing
import os
import pickle
import random

from utparking.lib.behavior_model import Policy, Runner

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def run_func(args):
    seed, policy = args
    random.seed(seed)
    runner = Runner(DATA_DIR, time_scale=10)
    runner.setup_run(stu_policy=policy)
    ret = runner.run()

    return ret


def run_exp(policy):
    num_runs = 8
    nums = [random.randint(0, 20480) for _ in range(num_runs)]
    if policy == 'smallest':
        p_enum = Policy.smallest
    elif policy == 'largest':
        p_enum = Policy.largest
    elif policy == 'closest':
        p_enum = Policy.closest
    elif policy == 'random':
        p_enum = Policy.random
    p_vec = [p_enum] * num_runs
    with multiprocessing.Pool(num_runs) as p:
        ret = p.map(run_func, zip(nums, p_vec))
    # ret = list(map(run_func, nums))

    with open(f"results/multirun_{policy}.pkl", "wb") as f:
        pickle.dump(ret, f)


def main():
    for policy in ['smallest', 'largest', 'closest', 'random']:
        run_exp(policy)


if __name__ == "__main__":
    main()
