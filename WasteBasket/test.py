import math
import random

import matplotlib.pyplot as plt
import numba
import numpy as np


# Accepted
def angle(n1, n2, D):
    """
    Calculate the angle of m1-D-n2
    """
    # Calculate the vectors between the points
    v1 = (n1[0] - D[0], n1[1] - D[1])
    v2 = (n2[0] - D[0], n2[1] - D[1])

    # Calculate the dot product of the vectors
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]

    # Calculate the lengths of the vectors
    v1_length = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    v2_length = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    # Calculate the cosine of the angle using the dot product and vector lengths
    cosine = dot_product / (v1_length * v2_length)

    # Calculate the angle in radians using the arccosine of the cosine
    radians = math.acos(cosine)

    return radians

def check_intersection(A, B, C, D):
    # Tính hệ số góc và hệ số điều chỉnh của đoạn thẳng AB
    if A[0] == B[0]:
        m1 = float('inf')
        c1 = A[0]
    else:
        m1 = (B[1] - A[1]) / (B[0] - A[0])
        c1 = A[1] - m1 * A[0]

    # Tính hệ số góc và hệ số điều chỉnh của đoạn thẳng CD
    if C[0] == D[0]:
        m2 = float('inf')
        c2 = C[0]
    else:
        m2 = (D[1] - C[1]) / (D[0] - C[0])
        c2 = C[1] - m2 * C[0]

    # Kiểm tra xem hai đoạn thẳng có cắt nhau hay không
    if m1 == m2:
        return False
    else:
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1
        if (min(A[0], B[0]) <= x <= max(A[0], B[0])) and (min(C[0], D[0]) <= x <= max(C[0], D[0])):
            return True
        else:
            return False


def test_angle():
    # Example data
    n1 = (1, -20)
    n2 = (1, 20)
    D = (2, 1)
    print(angle(n1, n2, D))

    # Create a scatter plot of the points
    fig, ax = plt.subplots()
    ax.scatter(*n1, color='blue', label='n1')
    ax.scatter(*n2, color='red', label='n2')
    ax.scatter(*D, color='green', label='D')
    # Add lines between D and n1, and between D and n2
    ax.plot([D[0], n1[0]], [D[1], n1[1]], color='blue')
    ax.plot([D[0], n2[0]], [D[1], n2[1]], color='red')

    # Add axis labels and legend
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

    # Show the plot
    plt.show()


def test(A, B):
    if A[0] == B[0]:
        m1 = np.inf
        c1 = A[0]
    else:
        m1 = (B[1] - A[1]) / (B[0] - A[0])
        c1 = A[1] - m1 * A[0]
    print("a =",m1, "b =", c1)


def test2(A, B):
    coeffs = np.polyfit([A[0], B[0]], [A[1], B[1]], 1)
    a, b = coeffs[0], coeffs[1]
    x, y = 1, 2
    # d = (a * x - y + b) / math.sqrt(a * a + 1)
    print(coeffs)

if __name__ == "__main__":
    # A = (random.randint(1, 100), random.randint(1, 100))
    # B = (random.randint(1, 100), random.randint(1, 100))
    # C = (random.randint(1, 100), random.randint(1, 100))
    # D = (random.randint(1, 100), random.randint(1, 100))
    # (82, 76), (61, 59), (82, 76), (19, 32)
    # print(numba.version_info)
    # A, B, C, D = (1, 1), (1, 2), (1, 1), (3, 1)
    # print(check_intersection(A, B, C, D))
    # plt.plot([A[0], B[0]], [A[1], B[1]], color='blue', label='AB')
    # plt.plot([C[0], D[0]], [C[1], D[1]], color='blue', label='CD')
    # plt.legend()
    # plt.show()
    # test2((1, 10), (1, 10))

    # while True:
    #     D = [random.randint(0, 100), random.randint(0, 100)]
    #     Gr = [random.randint(0, 100), random.randint(0, 100)]
    #     if not (D[0] == Gr[0] and D[1] == Gr[1]):
    #         try:
    #             coeffs = np.polyfit([0, Gr[0]], [0, Gr[1]], 1)
    #         except:
    #             print(D, Gr)
    #             exit(-1)

    test([2, 1], [2, 2])
    test([1, 1], [2, 1])
