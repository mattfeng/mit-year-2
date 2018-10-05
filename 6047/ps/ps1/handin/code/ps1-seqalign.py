#!/usr/bin/env python

from __future__ import print_function
import sys

base_idx = {
    'A': 0,
    'G': 1,
    'C': 2,
    'T': 3
}

PTR_NONE, PTR_GAP1, PTR_GAP2, PTR_BASE = 0, 1, 2, 3

def seqalignDP(seq1, seq2, subst_matrix, gap_pen):
    """
        Return the score of the optimal Needleman-Wunsch alignment for seq1 and seq2
        Note: gap_pen should be positive (it is subtracted)
    """
    F = [[0 for j in range(len(seq2) + 1)] for i in range(len(seq1) + 1)]
    TB = [[PTR_NONE for j in range(len(seq2) + 1)] for i in range(len(seq1) + 1)]

    # initialize dynamic programming table for Needleman-Wunsch alignment (Durbin p.20)
    for i in range(1, len(seq1) + 1):
        F[i][0] = 0 - i * gap_pen
        TB[i][0] = PTR_GAP2 # indicates a gap in seq2
    for j in range(1, len(seq2) + 1):
        F[0][j] = 0 - j * gap_pen
        TB[0][j] = PTR_GAP1 # indicates a gap in seq1

    # Fill in the dynamic programming tables F and TB, starting at [1][1]
    # Hints: The first row and first column of the table F[i][0] and F[0][j] are dummies
    #        (see for illustration Durbin p.21, Figure 2.5, but be careful what you
    #         think of as rows and what you think of as columns)
    #        Hence, the bases corresponding to F[i][j] are actually seq1[i-1] and seq2[j-1].
    #        Use the dictionary base_idx to convert from the character to an index to
    #         look up entries of the substitution matrix.
    #        To get started, you can complete and run the algorithm filling in only F,
    #         and then figure out how to do TB.

    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            b1 = seq1[i - 1]
            b2 = seq2[j - 1]
            opt1 = F[i - 1][j - 1] + subst_matrix[base_idx[b1]][base_idx[b2]] # i, j align
            opt2 = F[i - 1][j] - gap_pen # i aligns with gap, so we want to align remainder of seq1
            opt3 = F[i][j - 1] - gap_pen # j aligns with gap, so we want to align remainder of seq2
            F[i][j], TB[i][j] = max((opt1, PTR_BASE), (opt2, PTR_GAP2), (opt3, PTR_GAP1), key=lambda x: x[0])
            # F[i][j], TB[i][j] = min((opt1, PTR_BASE), (opt2, PTR_GAP2), (opt3, PTR_GAP1), key=lambda x: x[0])

    return F[len(seq1)][len(seq2)], F, TB

def traceback(seq1, seq2, TB):
    s1 = ""
    s2 = ""

    i = len(seq1)
    j = len(seq2)

    while TB[i][j] != PTR_NONE:
        if TB[i][j] == PTR_BASE:
            s1 = seq1[i-1] + s1
            s2 = seq2[j-1] + s2
            i=i-1
            j=j-1
        elif TB[i][j] == PTR_GAP1:
            s1 = '-' + s1
            s2 = seq2[j-1] + s2
            j=j-1
        elif TB[i][j] == PTR_GAP2:
            s1 = seq1[i-1] + s1
            s2 = '-' + s2
            i=i-1
        else:
            assert False

    return s1,s2

def readSeq(filename):
    """reads in a FASTA sequence"""

    stream = open(filename)
    seq = []

    for line in stream:
        if line.startswith(">"):
            continue
        seq.append(line.rstrip())

    return "".join(seq)

S = [
    # A   G   C   T
    [ 3, -1, -2, -2], # A
    [-1,  3, -2, -2], # G
    [-2, -2,  3, -1], # C
    [-2, -2, -1,  3]  # T
]
gap_pen = 4

# S = [
#     # A   G   C   T
#     [0, 1, 2, 2], # A
#     [1, 0, 2, 2], # G
#     [2, 2, 0, 1], # C
#     [2, 2, 1, 0]  # T
# ]
# gap_pen = -4

def main():
    # parse commandline
    if len(sys.argv) < 3:
        print("Syntax: python ps1-seqalign.py <FASTA 1> <FASTA 2>")
        quit()

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    seq1 = readSeq(file1)
    seq2 = readSeq(file2)

    score, F, TB = seqalignDP(seq1, seq2, S, gap_pen)

    print("Score: %d" % score)

    s1, s2 = traceback(seq1, seq2, TB)
    print(s1)
    print(s2)

    print("F(i, j):")

    for f in F:
        print("".join(map(lambda x: "%6s" % x, f)))

    print("Traceback:")

    for tb in TB:
        print("\t".join(map(str, tb)))

if __name__ == "__main__":
    main()
