import numpy as np
from numba.typed import Dict
from numba import njit

@njit(cache=True)
def top_K_nearest(distance_matrix, k=5):
    """
    Find the top k nearest for each point (including depot)
    :param distance_matrix: Distance matrix of each point
    :param k: K of nearest (EXCLUDING the depot AND itself)
    :return: a matrix A with size of no.point x k
    """
    if k >= len(distance_matrix[0]):
        print("Error: k must be lower or equal to the number of customers")

    A = np.zeros((len(distance_matrix), k), dtype=np.int64)
    for customer_i in range(len(A)):
        sort_customer = np.argsort(distance_matrix[customer_i][1:]) + 1
        if customer_i == 0:
            A[customer_i][:] = sort_customer[:k]
        else:
            A[customer_i][:] = sort_customer[1:k+1]
    return A


@njit(cache=True)
def create_dictionary_customer_route(solution):
    """
    Create a map between customer and route
    :param solution:
    :return: A Dictionary that map each customer with corresponding route
    """
    customer_map = Dict.empty(key_type= np.int64, value_type=np.int64)
    for route_i in range(len(solution)):
        customer_j = 1
        # 0 is depot. No need to be stored to the dictionary
        while solution[route_i][customer_j] != 0:
            customer_map[solution[route_i][customer_j]] = route_i
            customer_j += 1
    return customer_map