import pickle

import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt


def load_student_data(pth):
    with open(pth, 'rb') as f:
        data = pickle.load(f)
    for run in data:
        num_checked, time_spent, _ = run
        for stu in range(len(num_checked)):
            yield num_checked[stu], time_spent[stu]


def make_bar_chart(flist, runs):
    new_dat = []
    for file in flist:
        data = load_student_data(file)
        data = np.array(list(data))
        new_dat.append(np.mean(data, axis=0))

    data = np.array(new_dat)
    print(data.shape)

    barWidth = 0.25
    fig, ax = plt.subplots(figsize=(7, 5))
    ax2 = ax.twinx()

    br1 = np.arange(len(runs))
    br2 = [x + (barWidth + 0.05) for x in br1]
    ax.bar(br1,
           data[:, 0],
           label='number of garages',
           width=barWidth,
           color='tab:orange')
    ax2.bar(br2,
            data[:, 1],
            label="wait time",
            width=barWidth,
            color='tab:blue')

    ax.set_ylabel("# Parking Areas")
    ax2.set_ylabel("Time (s)")

    a = mpatches.Patch(color='tab:orange', label='Number of areas checked')
    b = mpatches.Patch(color='tab:blue', label='Mean Parking Time')

    plt.xticks([r + (barWidth + 0.05) / 2 for r in range(len(runs))], runs)
    plt.legend(handles=[a, b])
    plt.title("Policy Evaluation")

    plt.savefig("results/bars.png", dpi=300)


def main():
    root = 'results/multirun_'
    file_pth = lambda f: root + f + '.pkl'

    runs = ['smallest', 'largest', 'closest', 'random']
    flist = map(file_pth, runs)
    # make_bar_chart(flist, runs)


if __name__ == "__main__":
    main()
