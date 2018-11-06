#!/usr/bin/env python

import numpy as np
import scipy as sp
import scipy.stats as stats
import argparse

ALPHA = 0.05

def main(n, m, k, s):
    """
    Args: 
        n (int): sample size (number of people)
        m (int): number of snps
        k (int): number of disease related snps
        s (float): standard dev of SNP effect size
    """

    # choose k of the m snps to be related to the disease
    disease_ix = np.random.choice(np.arange(m), size=k, replace=False)
    print("Disease SNP indices: {}".format(sorted(disease_ix)))

    # generate betas
    betas = np.zeros(m)
    betas[disease_ix] = np.random.randn(k) * s
    betas = betas.reshape(-1, 1) # betas is now a column vec
    print("Betas:\n{}".format(betas.reshape(1, -1)))

    # generate genotypes where each snp has
    # prob 0.05 of being 1
    # (n x m) matrix
    genotypes = np.random.uniform(low=0.0, high=1.0, size=(n, m))
    genotypes = np.where(genotypes <= 0.05, 1, 0)
    print("Genotypes:\n{}".format(genotypes))

    # generate environmental influence "noise" for each
    # of the n people (n x 1) column vector
    epsilons = np.random.randn(n, 1)

    # phenotype expression (a floating value)
    # for each of n people (n x 1) column vector
    phenotypes = genotypes@betas + epsilons

    # boolean value whether or not they are affected (n x 1) column
    affected = np.where(phenotypes >= 2, 1, 0)
    frac_affected = np.asscalar(np.mean(affected, axis=0))

    # print("Affected:\n{}".format(affected))
    print("Fraction affected: {}".format(frac_affected))

    # compute chi-squared statistics for each of the m SNPs
    num_affected = np.sum(affected)
    num_unaffected = n - num_affected

    TP = 0
    TN = 0
    FP = 0
    FN = 0

    chi_squareds = np.zeros(m)
    for snp_ix in range(0, m):
        snp_0 = genotypes[:, snp_ix] == 0 # which ppl snp = 0
        snp_1 = genotypes[:, snp_ix] == 1 # which ppl snp = 1

        num_snp_0 = np.sum(snp_0)
        num_snp_1 = np.sum(snp_1)
        num_affected_snp_0 = np.sum(affected[snp_0])
        num_affected_snp_1 = np.sum(affected[snp_1])
        num_unaffected_snp_0 = num_snp_0 - num_affected_snp_0
        num_unaffected_snp_1 = num_snp_1 - num_affected_snp_1

        expected_affected_snp_0 = frac_affected * num_snp_0
        expected_unaffected_snp_0 = (1 - frac_affected) * num_snp_0
        expected_affected_snp_1 = frac_affected * num_snp_1
        expected_unaffected_snp_1 = (1 - frac_affected) * num_snp_1

        chi2_stat = (num_affected_snp_0 - expected_affected_snp_0) ** 2 / (expected_affected_snp_0) + \
                    (num_unaffected_snp_0 - expected_unaffected_snp_0) ** 2 / (expected_unaffected_snp_0) + \
                    (num_affected_snp_1 - expected_affected_snp_1) ** 2 / (expected_affected_snp_1) + \
                    (num_unaffected_snp_1 - expected_unaffected_snp_1) ** 2 / (expected_unaffected_snp_1)
        crit = stats.chi2.ppf(q=1 - (ALPHA / m), df=1)

        stat_sig = chi2_stat >= crit
        true_sig = snp_ix in disease_ix
        
        print("{:>3d}: {:6.2f} {:>3d} {:>3d}".format(snp_ix, chi2_stat, stat_sig, true_sig))

        if stat_sig and true_sig:
            TP += 1
        if stat_sig and not true_sig:
            FP += 1
        if not stat_sig and true_sig:
            FN += 1
        if not stat_sig and not true_sig:
            TN += 1
    
    print("TP: {}".format(TP))
    print("FP: {}".format(FP))
    print("TN: {}".format(TN))
    print("FN: {}".format(FN))
    acc = (TP + TN) / (TP + TN + FP + FN)
    prec = (TP) / (TP + FP)
    recall = (TP) / (TP + FN)
    print("Acc: {:>6.3f} Prec: {:>6.3f} Recall: {:>6.3f}".format(
        acc, prec, recall
    ))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "num_people",
        help="Number of genotypes to generate",
        type=int
    )
    parser.add_argument(
        "num_snps",
        help="Number of SNPs in total",
        type=int
    )
    parser.add_argument(
        "num_disease_snps",
        help="Number of SNPs that are disease related",
        type=int
    )
    parser.add_argument(
        "beta_stdev",
        help="Standard deviation of effect size of each of the disease related SNPs",
        type=float
    )
    parser.add_argument(
        "-s", "--seed",
        help="Random seed to make testing easier during development",
        type=int
    )

    args = parser.parse_args()

    if args.seed:
        print("Setting seed: {}".format(args.seed))
        np.random.seed(args.seed)

    main(args.num_people,
         args.num_snps,
         args.num_disease_snps,
         args.beta_stdev)