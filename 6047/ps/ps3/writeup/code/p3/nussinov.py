import numpy as np

def nussinov(seq):
    scoring_matrix = [
        # A   C   G   U
        [ 0,  0,  0, -1], # A  
        [ 0,  0, -1,  0], # C
        [ 0, -1,  0, -1], # G
        [-1,  0, -1,  0]  # U
    ]
    b2i = {
        "A": 0,
        "C": 1,
        "G": 2,
        "U": 3
    }

    memo = [[None] * len(seq) for _ in range(len(seq))]

    def S(i, j):
        r1 = b2i[seq[i]]
        r2 = b2i[seq[j]]
        
        a = memo[i][j - 1]
        b = memo[i + 1][j]
        c = scoring_matrix[r1][r2] + memo[i + 1][j - 1]
        d = [memo[i][k] + memo[k + 1][j] for k in range(i + 1, j - 1)]
        opt = min(a, b, c, *d)
        memo[i][j] = opt
    
    for i in range(0, len(seq)):
        memo[i][i] = 0

    for i in range(0, len(seq) - 1):
        memo[i + 1][i] = 0
    
    for i in range(len(seq) - 1, -1, -1):
        for j in range(i + 1, len(seq)):
            S(i, j)
    
    return memo[0][len(seq) - 1]
