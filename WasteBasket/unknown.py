import time

import numpy as np
from numba import njit
def difficult(A):
    array = [];
    df = 0;
    for j in range(0, len(A[0])):
        sum = 0;
        for i in range(0, len(A)):
            sum = sum + A[i][j];
        df = sum / len(A);
        array.append(df);
    return (array);

@njit(cache=True)
def difficult2(A):
    return np.sum(A, axis=0)


A = np.random.randint(1, 100, (10000, 10000))
# t1 = time.process_time()
# difficult(A)
t2 = time.process_time()
difficult2(A)
t3 = time.process_time()
# print("Time execute original =", t2 - t1)
print("Time execute numpy =", t3 - t2)