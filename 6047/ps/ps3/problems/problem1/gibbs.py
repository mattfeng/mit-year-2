#!/usr/bin/env python
# Use python3!

import sys
import string
import random
import numpy as np
from itertools import count
from collections import Counter

#### INSTRUCTIONS FOR USE:
# call program as follows: ./gibbs.py <Motif Length> <Data File>
# make sure the gibbs.py is marked as executable: chmod +x gibbs.py

alphabet = {
    "A": 0,
    "G": 1,
    "C": 2,
    "T": 3
}

def gibbs_sampler(S, L):
    """
    Performs Gibbs sampling on the sequences S in order to find the most probable
    motifs of length L.

    Args:
        S ([str]): list of sequences
        L (int): length of motif
    
    Returns:
        PWM (4xL list): frequencies of each base at each position.
                        Order of bases should be consistent with alphabet variable
    """

    PWM = np.array([])

    # randomly position initial motifs
    pos = [random.randint(0, len(seq) - L) for seq in S]

    # score correction by average frequency in dataset
    Bs = {seq:Counter(seq) for seq in S}

    for t in count():
        old = np.copy(pos)
        ordering = list(range(len(S)))
        random.shuffle(ordering)
        for i in ordering: # i is the sequence to exclude
            # print(f"[i] excluding {i}")
            Si = S[:i] + S[i + 1:]
            posi = pos[:i] + pos[i + 1:]
            PWM = build_profile(Si, posi, L) # PWM
            match = matching_distribution(S[i], PWM, L, Bs[S[i]])
            pos[i] = np.random.choice(np.arange(len(match)), p=match / np.sum(match))
            # pos[i] = np.argmax(match / np.sum(match))
        
        if (t > 50 and np.all(old == pos)) or t > 100:
            break
    
    print(f"[i] steps until convergence: {t}")

    return PWM, pos

def build_profile(S, pos, L):
    PWM = []
    for _ in range(len(alphabet)):
        PWM.append([0.0025] * L)
    
    PWM = np.array(PWM)

    for p, seq in zip(pos, S):
        for ix, residue in enumerate(seq[p:p + L]):
            PWM[alphabet[residue], ix] += 1
    
    PWM = PWM / (0.01 + len(S))
    
    return PWM

def matching_distribution(seq, Q, L, B):
    """
    Args:
        seq (str):
        Q (len(alphabet) x L float mtx): the profile matrix (PWM)
        L (int)
    """

    def score(motif):
        prob = 1
        for ix, res in enumerate(motif):
            prob *= Q[alphabet[res], ix] / (B[res] / len(seq))
        return prob
    
    scores = []

    for i in range(0, len(seq) - L + 1):
        scores.append(score(seq[i:i + L]))
    
    return np.array(scores)

def main():
    L = int(sys.argv[1])
    datafile = sys.argv[2]
    S = readdata(datafile)

    P, pos = gibbs_sampler(S,L)

    print("    ", end="")
    for i in range(L):
        print("{:<6d} ".format(i + 1), end="")
    print()

    for key, val in alphabet.items():
        print(" {} ".format(key), end="")
        for i in range(L):
            print(" {:5.3f} ".format(P[val, i]), end="")
        print()

def readdata(file):
    data = []
    for line in open(file,'r'):
        data.append(line[:-1])
    return data

if __name__ == "__main__":
    # S = [
    #     "AAGGCCTT", # AA
    #     "AGAGAGAG", # GA
    #     "CCCCCGGG", # CC
    #     "ACACACAG", # CA
    #     "GTGGGGGG"  # GG
    # ]
    # L = 2
    # print(gibbs_sampler(S, L))

    main()