#!/usr/bin/env python

import numpy as np
from nussinov import nussinov
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

def avg_score(L, p, iters=1000):
    """
    L (int): length of RNA sequence
    p (float): fraction of AU
    """
    scores = []
    for i in range(iters):
        seq = "".join(np.random.choice(list("ACGU"), L, p=[(1 - p) / 2, p / 2, p / 2, (1 - p) / 2]))
        score = nussinov(seq)
        # print(f"[i] iteration {i}: score = {score}")
        scores.append(score)
    
    return np.mean(scores)

def main():
    lengths = np.arange(10, 150, 10)
    probs = np.linspace(0, 1, 20)

    # avg_scores = np.zeros(len(lengths))

    # for ix, L in enumerate(lengths):
    #     avg = avg_score(L, 0.5)
    #     avg_scores[ix] = avg
    #     print(f"length: {L}, score: {avg}")

    # plt.plot(lengths, avg_scores)
    # plt.show()

    avg_scores = np.zeros(len(probs))

    for ix, p in enumerate(probs):
        avg = avg_score(100, p)
        avg_scores[ix] = avg
        print(f"fraction: {p}, score: {avg}")

    plt.plot(probs, avg_scores)
    plt.show()

if __name__ == "__main__":
    main()

