import pickle

import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from utparking.lib.behavior_model import State
sns.set_theme(style="darkgrid")


def load_stats_data(pth):
    with open(pth, 'rb') as f:
        data = pickle.load(f)
    ret = None
    for run in data:
        for i in range(len(run)):
            run[i].update({'tick': i})
        if ret is None:
            ret = pd.DataFrame(run)
        else:
            ret = pd.concat((ret, pd.DataFrame(run)), ignore_index=True)
        
    return ret


def main():
    root = 'results/multirun_times_'
    file_pth = lambda f: root + f + '.pkl'

    runs = ['smallest', 'largest', 'closest', 'random']
    convergence_times = {
        'smallest': 5125.25,
        'largest': 4973.375,
        'closest': 3894.875,
        'random': 1040.0
    }
    flist = map(file_pth, runs)

    pds = list(map(load_stats_data, flist))

    fig, ax = plt.subplots(4, figsize=(3.8*2, 4.6*2))
    for i in range(4):
        a = sns.lineplot(ax=ax[i], data=pds[i], x="tick", y=State.searching, label="Searching", errorbar=None, legend=False)
        b = sns.lineplot(ax=ax[i], data=pds[i], x="tick", y=State.traveling, label="Traveling", errorbar=None, legend=False)
        c = sns.lineplot(ax=ax[i], data=pds[i], x="tick", y=State.parking, label="Parking", errorbar=None, legend=False)
        d = sns.lineplot(ax=ax[i], data=pds[i], x="tick", y=State.parked, label="Parked", errorbar=None, legend=False)
        e = sns.lineplot(ax=ax[i], data=pds[i], x="tick", y=State.stuck, label="Stuck", errorbar=None, legend=False)
        f = ax[i].axhline(y=20_510, linestyle='--', label="Max Parking")
        g = ax[i].axvline(x=convergence_times[runs[i]], linestyle='-', label="Convergence", c='tab:red')
        ax[i].set_xlim([0,5200])
        ax[i].set_yticks(np.arange(start=0, stop=35000, step=10000))
        
        ax[i].set_xlabel("Time (s)")
        ax[i].set_ylabel("# Students")
        ax[i].set_title(f"policy: {runs[i]}")
    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.legend(lines[:7], labels[:7], loc='lower center', ncol=3)
    plt.subplots_adjust(hspace=0.6, bottom=0.15, top=0.95)
    plt.savefig('results/large.png', dpi=300)
    
def get_stats():
    def load_data(pth):
        with open(pth, 'rb') as f:
            data = pickle.load(f)
        ret = []
        for run in data:
            for i in range(len(run)):
                run[i].update({'tick': i})
            ret.append(pd.DataFrame(run))
        return ret

    root = 'results/multirun_times_'
    file_pth = lambda f: root + f + '.pkl'

    runs = ['smallest', 'largest', 'closest', 'random']
    flist = map(file_pth, runs)

    pds = list(map(load_data, flist))

    for i in range(len(runs)):
        nps = map(lambda f: f.get(State.parked).to_numpy(), pds[i])
        maxs = map(lambda f: np.argmax(f), nps)
        means = np.mean(list(maxs))
        print(f"convergence occured at {means} for {runs[i]}")
    # print(pds[0][0].get(State.parked).to_numpy())


if __name__ == "__main__":
    main()
    # get_stats()
