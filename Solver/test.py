import time

from numba import njit
import numpy as np
from Solver.Instances.Instance import load_data
from Solver.Algorithm.NearestNeighbor import get_initial_solution
from Solver.Algorithm.DestroyOperator.RandomDestroy import random_destroy_v2
from Solver.Algorithm.DestroyOperator.ShawDestroy import  shaw_destroy_v2
from Solver.Algorithm.DestroyOperator.MassiveDestroy import massive_destroy_v2
from Solver.Algorithm.DestroyOperator.WorstDestroy import worst_destroy_v2
from Solver.Algorithm.RepairOperator import *
from Solver.Instances.Route import erase, insert
import matplotlib.pyplot as plt
import sys
from numba import objmode


def test():
    a = [1, 2, 3, 4]
    b = [2, 3, 4 ,5]
    plt.plot(a, b)
    plt.show()


@njit()
def test2():
    a = np.array([1.2, 2.3, 3.4])
    with objmode():
        a[0] = time.process_time()
        a[1] = time.process_time()
    print(a)
    print(a[1] - a[0])

test2()


"""
optimal, vehicles, capacity, demand, x, y, distance_matrix = load_data("A-n32-k5")
solution, route_length, route_costs, route_load = get_initial_solution(vehicles, capacity, demand, distance_matrix)
removed = np.zeros(len(demand), dtype=np.int32)
print(solution)
print()

while route_length[0] > 2:
    erase(1, 0, solution, route_length, route_costs, route_load, demand, distance_matrix)

insert(30, 0, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(26, 1, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(16, 2, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(12, 3, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(1, 4, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(7, 5, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(14, 6, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(29, 7, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(22, 8, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
insert(18, 9, 0, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix)
"""
