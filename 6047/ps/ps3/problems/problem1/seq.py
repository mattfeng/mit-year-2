data1 = """
0.999  0.000  0.000  0.000  0.000  0.999  0.999  0.000  0.000  0.000
0.000  0.000  0.000  0.000  0.999  0.000  0.000  0.000  0.000  0.000
0.000  0.000  0.000  0.999  0.000  0.000  0.000  0.000  0.000  0.999
0.000  0.999  0.999  0.000  0.000  0.000  0.000  0.999  0.999  0.000
""".strip().split("\n")

data2 = """
0.555  0.334  1.000  0.333  0.000  0.111  0.444  0.000  0.000  0.000
0.111  0.333  0.000  0.000  0.000  0.000  0.556  0.000  0.000  0.000
0.000  0.222  0.000  0.000  1.000  0.222  0.000  0.000  0.777  0.000
0.334  0.111  0.000  0.667  0.000  0.667  0.000  1.000  0.223  1.000

""".strip().split("\n")

data3 = """
0.000  0.000  0.000  0.000  0.091  0.152  0.182  0.000  0.000  0.000
0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.061  0.000  0.303
0.000  0.364  0.364  0.121  0.000  0.333  0.000  0.000  0.424  0.000
1.000  0.636  0.636  0.879  0.909  0.515  0.818  0.939  0.576  0.697
""".strip().split("\n")

data4 = """
0.036  0.127  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000
0.000  0.000  0.000  0.109  0.000  0.182  0.000  0.000  0.000  0.000
0.182  0.000  0.236  0.000  0.364  0.091  0.273  0.364  0.000  0.345
0.782  0.873  0.764  0.891  0.636  0.727  0.727  0.636  1.000  0.655
""".strip().split("\n")

import numpy as np

seqs = [[" "] * 10 for _ in range(1000)]
freqs = []
for line in data4:
    freqs.append(list(map(lambda x: int(1000 * float(x)), line.split("  "))))

freqs = np.array(freqs).T

for ix, freq in enumerate(freqs):
    for i in range(1000):
        chars = freq[0] * "A" + freq[1] * "G" + freq[2] * "C" + freq[3] * "T"
        seqs[i][ix] = chars[i]

for seq in seqs:
    print("".join(seq))