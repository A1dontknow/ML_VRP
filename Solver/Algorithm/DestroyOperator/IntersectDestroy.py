from random import randint

import numpy as np

from Solver.Instances.Route import erase, check_intersection
from numba import njit


@njit(cache=True)
def intersect_destroy(x, y, solution, route_length, route_costs, route_load, demand, distance_matrix, removed):
    # Chọn ra 1 tuyến để phá hủy
    random_route = randint(0, len(solution) - 1)
    while route_length[random_route] <= 3:
        random_route = randint(0, len(solution) - 1)

    # Chọn ra 2 khách hàng liền kề, nếu cắt nhau sẽ tiến hành loại 4 khách hàng tương ứng 2 đường cắt nhau
    for i in range(1, route_length[random_route] - 2):
        customer_a = solution[random_route][i]
        customer_b = solution[random_route][i + 1]
        # Tìm 2 khách hàng cd giao ab
        for route in range(len(solution)):
            if route != random_route and route_length[route] > 3:
                for customer in range(1, route_length[route] - 2):
                    customer_c = solution[route][customer]
                    customer_d = solution[route][customer + 1]
                    if check_intersection((x[customer_a], y[customer_a]), (x[customer_b], y[customer_b]), (x[customer_c], y[customer_c]), (x[customer_d], y[customer_d])):
                        removed[0], removed[1], removed[2], removed[3] = customer_a, customer_b, customer_c, customer_d
                        # print(removed)
                        # print(solution[random_route][i])
                        erase(i, random_route, solution, route_length, route_costs, route_load, demand, distance_matrix)
                        # print(solution[random_route][i])
                        erase(i, random_route, solution, route_length, route_costs, route_load, demand, distance_matrix)
                        # print(solution[route][customer])
                        erase(customer, route, solution, route_length, route_costs, route_load, demand, distance_matrix)
                        # print(solution[route][customer])
                        erase(customer, route, solution, route_length, route_costs, route_load, demand, distance_matrix)
                        # print(np.sum(route_length))
                        return
