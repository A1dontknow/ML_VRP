import numpy as np
from matplotlib import pyplot as plt
from numba import njit, objmode
import random


@njit(cache=True)
def numba_choice(population, weights, k):
    # Get cumulative weights
    wc = np.cumsum(weights)
    # Total of weights
    m = wc[-1]
    # Arrays of sample and sampled indices
    sample = np.empty(k, population.dtype)
    sample_idx = np.full(k, -1, np.int32)
    # Sampling loop
    i = 0
    while i < k:
        # Pick random weight value
        r = m * np.random.rand()
        # Get corresponding index
        idx = np.searchsorted(wc, r, side='right')
        # Check index was not selected before
        # If not using Numba you can just do `np.isin(idx, sample_idx)`
        for j in range(i):
            if sample_idx[j] == idx:
                continue
        # Save sampled value and index
        sample[i] = population[idx]
        sample_idx[i] = population[idx]
        i += 1
    return sample


@njit
def rand_choice_nb(arr, prob):
    """
    :param arr: A 1D numpy array of values to sample from.
    :param prob: A 1D numpy array of probabilities for the given samples.
    :return: A random sample from the given array with a given probability.
    """
    return arr[np.searchsorted(np.cumsum(prob), np.random.random(), side="right")]


@njit
def stupid_test():
    return np.random.choice(np.arange(7), 2, replace=False)

ITERATION = 10000
@njit
def test():
    with objmode(iteration='int64'):
        iteration = ITERATION
    print(iteration)

# print out 10000
test()
ITERATION = 20000
# print out 20000
test()

# a = np.array([7, 8, 9, 10])
# b = np.array([0.2, 0.8])
# x = np.linspace(0, 2, 2001).round(3)
# y = np.linspace(0, 2, 2001).round(3)
# plt.plot(x, y)
# plt.show()
