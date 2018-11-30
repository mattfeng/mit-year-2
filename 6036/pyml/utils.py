#!/usr/bin/env python

import numpy as np
import itertools

def cv(value_list):
    return np.array(value_list).reshape((-1, 1))

def rv(value_list):
    return np.array(value_list).reshape((1, -1))

def _len(vec):
    return np.linalg.norm(vec)

def hat(vec):
    return vec / _len(vec)

def oh(x, k):
    """
    Returns a one-hot column vector for feature x 
        with k classes.
    :param x: The value of the feature
    :param k: The number of classes
    """
    vec = np.zeros(k)
    vec[x] = 1
    return vec.reshape((-1, 1))

def polyfeatures(order):
    # raw_features is d by n
    # return is D by n where D = sum_{i = 0}^order  multichoose(d, i)
    def f(raw_features):
        d, n = raw_features.shape
        result = []   # list of column vectors
        for j in range(n):
            features = []
            for o in range(order+1):
                indexTuples = \
                          itertools.combinations_with_replacement(range(d), o)
                for it in indexTuples:
                    features.append(mul(raw_features[i, j] for i in it))
            result.append(cv(features))
        return np.hstack(result)
    return f