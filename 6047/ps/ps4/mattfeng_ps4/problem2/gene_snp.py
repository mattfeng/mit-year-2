#!/usr/bin/env python

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import sys
import time

exp_data = pd.read_csv("./ExpData.txt", sep="\t")
exp_data = exp_data.set_index("Patient")
snp_data = pd.read_csv("./SnpData.txt", sep="\t")
snp_data = snp_data.set_index("Patient")

# generate table of R2 scores where
# R2_scores.ix[i, j] = 
#     R2 score of correlation
#     between SNP i and GENE j
LO = int(sys.argv[1])
HI = int(sys.argv[2])

# Turns out initializing too large of a
# DataFrame makes it really slow --
# likely writing to a swapfile or the like
R2_scores = pd.DataFrame(
    index=["SNP_{}".format(ix) for ix in range(LO, HI)],
    columns=exp_data.columns)

# snps range from 1 to 500
for snp_ix in range(LO, HI):
    snp = "SNP_{}".format(snp_ix)
    x = snp_data.loc[:, snp].values.reshape(-1, 1)
    print("[i] processing snp: {}".format(snp))
    for gene in exp_data.columns:
        start = time.time()
        y = exp_data.loc[:, gene].values.astype(np.float32)
        reg = LinearRegression().fit(x, y)
        score = reg.score(x, y) # compute the R2 score
        R2_scores.loc[snp, gene] = score
        end = time.time()
        # print("[i] gene: {} {:>6.2f}".format(gene, end - start))
        
R2_scores.to_csv("gene_snp_scores_{}_{}.txt".format(LO, HI), header=True, index=True)