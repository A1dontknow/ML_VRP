import math

import numpy as np
from numba import njit


@njit(cache=True)
def linear_coeff(A, B):
    if A[0] == B[0]:
        a = np.inf
        b = A[0]
    else:
        a = (B[1] - A[1]) / (B[0] - A[0])
        b = A[1] - a * A[0]
    return a, b


@njit(cache=True)
def check_intersection(A, B, C, D):
    if A == C or A == D or B == C or B == D:
        return False
    # Tính hệ số góc và hệ số điều chỉnh của đoạn thẳng AB
    m1, c1 = linear_coeff(A, B)
    # Tính hệ số góc và hệ số điều chỉnh của đoạn thẳng CD
    m2, c2 = linear_coeff(C, D)

    # Kiểm tra xem hai đoạn thẳng có cắt nhau hay không
    if m1 == m2:
        return False
    else:
        x = (c2 - c1) / (m1 - m2)
        # y = m1 * x + c1
        if (min(A[0], B[0]) <= x <= max(A[0], B[0])) and (min(C[0], D[0]) <= x <= max(C[0], D[0])):
            # print(A, B, C, D)
            return True
        else:
            return False


# Tìm số điểm giao giữa route r_i và route r_j
def I(r_i, r_j):
    intersect = 0
    for i in range(0, len(r_i) - 1):
        a = r_i[i].xy
        b = r_i[i + 1].xy
        for j in range(0, len(r_j) - 1):
            c = r_j[j].xy
            d = r_j[j + 1].xy
            if check_intersection(a, b, c, d):
                intersect += 1
    return intersect


@njit(cache=True)
def rad(n1, n2, D):
    """
    Tính góc m1-D-n2 theo radian. n1, n2, D là tuple (x, y) trong không gian 2 chiều
    """
    # Calculate the vectors between the points
    v1 = (n1[0] - D[0], n1[1] - D[1])
    v2 = (n2[0] - D[0], n2[1] - D[1])

    # Calculate the dot product of the vectors
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]

    # Calculate the lengths of the vectors
    v1_length = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    v2_length = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    if v1_length == 0 or v2_length == 0:
        return 0

    # print(v1_length, v2_length)
    # Calculate the cosine of the angle using the dot product and vector lengths
    cosine = dot_product / (v1_length * v2_length)
    # PRevent StUp1D error calculation
    if cosine > 1.0:
        cosine = 1.0
    # Calculate the angle in radians using the arccosine of the cosine
    radians = math.acos(cosine)

    return radians


def avg_width_route(route, Gr):
    D = route[0].xy
    # Phuong trinh duong thang qua D va Gr. coeffs: y = ax + b
    if D[0] == Gr[0] and D[1] == Gr[1]:
        return 0
    a, b = linear_coeff(D, Gr)
    minimum, maximum = 9999999, -9999999
    for c in range(1, len(route) - 1):
        x, y = route[c].xy
        # special case
        if a == np.inf:
            d = (x - b)
        else:
            # y = ax + b => ax - y + b = 0
            d = (a * x - y + b) / math.sqrt(a * a + 1)
        if maximum < d:
            maximum = d
        if minimum > d:
            minimum = d
    return maximum - minimum

# print(check_intersection((82, 76), (98, 14), (88, 51), (96, 44)))
if __name__ == "__main__":
    # Case for line 68
    print(rad((22, 22), (18, 18), (35, 35)))