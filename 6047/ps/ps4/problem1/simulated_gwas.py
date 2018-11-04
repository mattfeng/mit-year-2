#!/usr/bin/env python

import numpy as np
import argparse

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
    print("Betas: {}".format(betas))

    # generate genotypes where each snp has
    # prob 0.05 of being 1
    # (n x m) matrix
    genotypes = np.random.uniform(low=0.0, high=1.0, size=(n, m))
    genotypes = np.where(genotypes <= 0.05, 1, 0)

    # generate environmental influence "noise" for each
    # of the n people (n x 1) column vector
    epsilons = np.random.randn(n, 1)

    # phenotype expression (a floating value)
    # for each of n people (n x 1) column vector
    phenotypes = genotypes@betas + epsilons

    # boolean value whether or not they are affected (n x 1) column
    affected = np.where(phenotypes >= 2, 1, 0)

    # compute chi-squared statistics


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