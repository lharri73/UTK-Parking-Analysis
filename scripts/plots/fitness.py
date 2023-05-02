import pickle

import matplotlib.pyplot as plt
import numpy as np


def parse_pops(pops):
    for pop in pops:
        cur = np.packbits(pop, axis=1)

        policy = (cur >> 16 & 0x3)
        speed_adj = ((cur & 0xff) / 256) + 0.5
        agressive = 2 * ((cur >> 8) & 0xff) / 256.0

        yield policy, speed_adj, agressive


def main():
    with open("meta.pkl", "rb") as f:
        data = pickle.load(f)

    means = data["means"]
    maxs = data["maxs"]
    fits = data["fits"]
    pops = data["pops"]

    plt.plot(means, label="mean")
    plt.plot(maxs, label="max")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
