from numba import njit
from Math_support import check_intersection


@njit(cache=True)
def can_insert(node_id, route_id, route_load, demand, capacity):
    """
    Hàm kiểm tra việc chèn vào route có khả thi hay không
    """
    return route_load[route_id] + demand[node_id] <= capacity


@njit(cache=True)
def erase(position, route_id, solution, route_length, route_costs, route_load, demand, distance_matrix):
    """
    Hàm thực hiện xóa khách hàng có vị trí là position từ tuyến route_id trong nghiệm
    Chi phí, tải trọng và số lượng khách trong tuyến sẽ được cập nhật sau khi xóa
    """
    prev = solution[route_id][position - 1]
    removing = solution[route_id][position]
    after = solution[route_id][position + 1]
    route_costs[route_id] += distance_matrix[prev][after] - distance_matrix[prev][removing] - distance_matrix[removing][after]
    route_load[route_id] -= demand[removing]
    route_length[route_id] -= 1
    while solution[route_id][position] != 0:
        solution[route_id][position] = solution[route_id][position + 1]
        position += 1


@njit(cache=True)
def erase_id(node_id, route_id, solution, route_length, route_costs, route_load, demand, distance_matrix):
    """
    Hàm thực hiện xóa khách hàng có ID là node_id từ tuyến route_id trong nghiệm
    Chi phí, tải trọng và số lượng khách trong tuyến sẽ được cập nhật sau khi xóa
    """
    for i in range(route_length[route_id]):
        if solution[route_id][i] == node_id:
            erase(i, route_id, solution, route_length, route_costs, route_load, demand, distance_matrix)
            break

@njit(cache=True)
def insert(node_id, position, route_id, solution, route_length, route_costs, route_load, demand, capacity, distance_matrix):
    """
    Hàm thực hiện chèn khách hàng có ID là node_id từ tuyến route_id trong nghiệm
    Chi phí, tải trọng và số lượng khách trong tuyến sẽ được cập nhật sau khi chèn
    """
    if can_insert(node_id, route_id, route_load, demand, capacity):
        route_length[route_id] += 1
        route_load[route_id] += demand[node_id]
        prev = solution[route_id][position]
        after = solution[route_id][position + 1]
        route_costs[route_id] += distance_matrix[prev][node_id] + distance_matrix[node_id][after] - distance_matrix[prev][after]
        for i in range(route_length[route_id], position + 1, -1):
            solution[route_id][i] = solution[route_id][i-1]
        solution[route_id][position + 1] = node_id


@njit(cache=True)
def erase_id_from_sol(node_id, solution, route_length, route_costs, route_load, demand, distance_matrix):
    for route_id in range(len(solution)):
        for j in range(route_length[route_id]):
            if solution[route_id][j] == node_id:
                erase(j, route_id, solution, route_length, route_costs, route_load, demand, distance_matrix)
                break


@njit(cache=True)
def I(x, y, r_i, len_r_i, r_j, len_r_j):
    intersect = 0
    for i in range(0, len_r_i - 1):
        a = (x[r_i[i]], y[r_i[i]])
        b = (x[r_i[i + 1]], y[r_i[i + 1]])
        for j in range(0, len_r_j - 1):
            c = (x[r_j[j]], y[r_j[j]])  #r_j[j].xy
            d = (x[r_j[j + 1]], y[r_j[j + 1]])  #r_j[j + 1].xy
            if check_intersection(a, b, c, d):
                intersect += 1
    return intersect


@njit(cache=True)
def penalty_s1(x, y, solution, route_length, alpha):
    return 0
    # # R = number of route
    # R = len(solution)
    # penalty = 0
    # for i in range(R - 1):
    #     for j in range(i + 1, R):
    #         intersect = I(x, y, solution[i], route_length[i], solution[j], route_length[j])
    #         if intersect > 0:
    #             penalty += intersect
    #
    # return alpha * penalty
