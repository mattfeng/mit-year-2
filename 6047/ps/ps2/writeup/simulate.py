import numpy as np
import math

N_model = {
    0:  0.10,
    1:  0.35,
    2:  0.25,
    3:  0.20,
    6:  0.10
}

C_model = {
    0: 0.05,
    1: 0.15,
    2: 0.2,
    3: 0.3,
    6: 0.3
}

def compare_seq(seq, model_a, model_b):
    log_prob_a = 0
    log_prob_b = 0
    
    for s in seq:
        log_prob_a += math.log(model_a[s])
        log_prob_b += math.log(model_b[s])

    return (log_prob_a, log_prob_b)
    
def generate_seq(model, l, N):
    seqs = []
    for i in range(N):
        seq = np.random.choice(
            list(model.keys()), 10, p=list(model.values()))
        seqs.append(seq)
    return seqs
    
# Part B
seqs = generate_seq(N_model, 10, 10000)
C_gt_N_count = 0
for seq in seqs:
    lp_N, lp_C = compare_seq(seq, N_model, C_model)
    if lp_C > lp_N:
        C_gt_N_count += 1

print("P(S | C) > P(S | N): {}".format(C_gt_N_count / 10000))

# Part C
seqs = generate_seq(C_model, 10, 10000)
N_gt_C_count = 0
for seq in seqs:
    lp_N, lp_C = compare_seq(seq, N_model, C_model)
    if lp_N > lp_C:
        N_gt_C_count += 1

print("P(S | N) > P(S | C): {}".format(N_gt_C_count / 10000))

"""
ACGACGACTA
CAGACGCTGA
TTCCTCTGAT
AGATGTGACT
"""
n, c = compare_seq(map(int, "0011110002"), N_model, C_model)
print("log P(S | N) = {}".format(n))
print("log P(S | C) = {}".format(c))

"""
ACAACGAGTA
AAAACGAATA
TCATCGAGTT
ACATCTAACT
"""
n, c = compare_seq(map(int, "3362636232"), N_model, C_model)
print("log P(S | N) = {}".format(n))
print("log P(S | C) = {}".format(c))