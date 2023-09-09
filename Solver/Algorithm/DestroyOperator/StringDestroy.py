import random
from numba import njit
from Solver.Instances.Route import erase_id_from_sol


@njit()
def string_destroy(to_remove, solution, route_length, route_costs, route_load, demand, distance_matrix, removed, top_k_nn):
    center = random.randint(1, len(solution))
    erase_id_from_sol(center, solution, route_length, route_costs, route_load, demand, distance_matrix)
    removed[0] = center
    it_removed = 1

    while it_removed < to_remove:
        erase_id_from_sol(top_k_nn[center][it_removed - 1], solution, route_length, route_costs, route_load, demand, distance_matrix)
        removed[it_removed] = top_k_nn[center][it_removed - 1]
        it_removed += 1
