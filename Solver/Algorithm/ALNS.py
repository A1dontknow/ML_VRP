import time

import numpy as np

import Solver.Config as Config
from numba import njit, objmode
from Solver.Algorithm import NearestNeighbor, LocalSearch, AdaptiveMechanism
from Solver.Algorithm.DestroyOperator import *
from Solver.Algorithm.DestroyOperator import StringDestroy, IntersectDestroy
from Solver.Algorithm.RepairOperator import *
from Solver.Algorithm.Util import *
from Solver.Instances.Route import penalty_s1


@njit(cache=True)
def solve_v2(x, y, vehicles, capacity, demand, distance_matrix, testing):
    """
    :param vehicles: Số phương tiện
    :param capacity: Tải trọng tối đa của mỗi xe
    :param demand: Nhu cầu mỗi khách hàng
    :param distance_matrix: Ma trận biểu diễn khoảng cách từng khách hàng
    :param testing: Experiment stuff. Delete that for cleaner code
    :return: Nghiệm tốt nhất tìm được và chi phí của nghiệm đó

    Ham nay giai bai toan CVRP bang thuat toan Adaptive Large Neighborhood Search. Ket qua thuat
    toan se phu thuoc vao cac tham so nam trong file /Instance/Config.py. Khi chay xong, ket qua
    se duoc luu vao /Dataset/Solution/<ten file>/
    """
    print()
    # Tricky way to use global variable in numba :)
    with objmode(iteration='int64', log='int8', early_stop='int8', best_known='float64', min_gap='float64', max_gap='float64', alpha='float64'):
        iteration = Config.ITERATION
        log = Config.PRINT_LOG
        early_stop = Config.EARLY_STOP
        best_known = Config.OPTIMAL
        min_gap = Config.MIN_GAP
        max_gap = Config.MAX_GAP
        alpha = Config.alpha


    # Các biến sử dụng cho cơ chế thích nghi
    # Operator quy ước theo thứ tự: Shaw - Random - Worst - Massive (Destroy) | Greedy - Random (Repair)
    destroy_operator = np.array([0, 1, 2])
    repair_operator = np.array([0, 1])

    destroy_weight = np.array([1, 1, 1])
    repair_weight = np.array([1, 1])

    destroy_score = np.array([0, 0, 0])
    repair_score = np.array([0, 0])

    destroy_used = np.array([0, 0, 0])
    repair_used = np.array([0, 0])

    # Setup biến cho Early stop. Sẽ không có tác dụng nếu không Early stop
    lb_cost = 0
    ub_cost = 9999999
    if early_stop:
        lb_cost = best_known * (1 + min_gap)
        ub_cost = best_known * (1 + max_gap)

    # Dựng nghiệm ban đầu
    solution, route_length, route_costs, route_load = NearestNeighbor.get_initial_solution(vehicles, capacity, demand, distance_matrix)

    # Khởi tạo nghiệm tốt nhất
    best_sol, best_cost = np.copy(solution), np.sum(route_costs)

    # removed lưu trữ những khách hàng bị xóa. ips là iterate per segment
    removed = np.zeros(len(demand) - 1, dtype=np.int32)
    to_remove = int(Config.DESTROY_RATIO * (len(demand) - 1))
    ips = iteration / Config.SEGMENT

    # Luu tru phuc vu cho slack string removal. But not used anymore
    # top_k_nn = top_K_nearest(distance_matrix, to_remove)
    # c_r_map = create_dictionary_customer_route(solution)

    # Base case cho Early stop
    if early_stop:
        if best_cost < lb_cost:
            # Worsen the solution by random destroy-repair
            while best_cost < lb_cost:
                s2, r_le2, r_c2, r_lo2 = np.copy(solution), np.copy(route_length), np.copy(route_costs), np.copy(
                    route_load)
                RandomDestroy.random_destroy_v2(to_remove, s2, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
                can_repair = RandomRepair.random_repair_v2(removed, s2, r_le2, r_c2, r_lo2, demand, capacity,
                                                           distance_matrix)
                if can_repair:
                    worsen_cost = np.sum(r_c2)
                    if worsen_cost > best_cost:
                        best_cost = worsen_cost
                        best_sol = np.copy(solution)
                    solution, route_length, route_costs, route_load = np.copy(s2), np.copy(r_le2), np.copy(
                        r_c2), np.copy(r_lo2)
                else:
                    removed.fill(0)

    if log:
        print("Ket qua sinh nghiem ban dau:")
        print(best_sol)
        print("ALNS Process...")
    test = 0

    # Sử dụng hiệu chỉnh phục vụ quá trình chạy ALNS
    best_reg_cost = best_cost + penalty_s1(x, y, solution, route_length, alpha)
    cur_cost, cur_reg = best_cost, best_reg_cost

    # Phục vụ sau này plot ra biểu đồ cost - thời gian. Mỗi 0.05s lấy best 1 lần. Tổng thời gian lấy là 10s
    bests = np.zeros(201)
    bests[0] = best_cost
    time_it = 1
    with objmode(start_time='float64'):
        start_time = time.process_time()

    cost_iterator = np.zeros(iteration)
    # Annoying stuff from early stop thingy. Delete it if no need early stop .-.
    if lb_cost <= best_cost <= ub_cost and early_stop:
        return best_sol, best_cost, bests, cost_iterator



    # Lặp thuật toán đến số lần nhất định
    for i in range(iteration):
        # test for operators experiment only
        cost_iterator[i] = best_cost
        # test dùng để thử nghiệm, là 1 phần của cơ chế chấp nhận nghiệm
        test += 1
        # sao chép nghiệm hiện tại để destroy/repair. Lỡ như ko repair được thì chẳng sao
        s2, r_le2, r_c2, r_lo2 = np.copy(solution), np.copy(route_length), np.copy(route_costs), np.copy(route_load)
        # Chọn cặp operator theo Roulette-wheel
        operators = AdaptiveMechanism.select_operator(destroy_operator, destroy_weight, repair_operator, repair_weight)

        # Phá nghiệm
        if operators[0] == 0:
            ShawDestroy.shaw_destroy_v2(to_remove, s2, Config.D, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
        elif operators[0] == 1:
            RandomDestroy.random_destroy_v2(to_remove, s2, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
        elif operators[0] == 2:
            if testing:
                IntersectDestroy.intersect_destroy(x, y, s2, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
            else:
                WorstDestroy.worst_destroy_v2(to_remove, s2, r_le2, r_c2, r_lo2, demand, distance_matrix, removed)
        # elif operators[0] == 3:
        #     MassiveDestroy.massive_destroy_v2(s2, r_le2, r_c2, r_lo2, removed)
            # StringDestroy.string_destroy(to_remove, s2, r_le2, r_c2, r_lo2, demand, distance_matrix, removed, top_k_nn)

        # Sửa nghiệm
        can_repair = False
        if operators[1] == 0:
            can_repair = GreedyRepair.greedy_repair_v2(removed, s2, r_le2, r_c2, r_lo2, demand, capacity, distance_matrix)
        elif operators[1] == 1:
            can_repair = RandomRepair.random_repair_v2(removed, s2, r_le2, r_c2, r_lo2, demand, capacity, distance_matrix)

        # Nếu nghiệm sửa thành công thì xét các trường hợp
        if can_repair:
            s2_cost, s2_regularize = np.sum(r_c2), penalty_s1(x, y, s2, r_le2, alpha)
            # Nếu nghiệm mới tốt hơn nghiệm cũ
            if s2_cost + s2_regularize < cur_cost + cur_reg and s2_cost >= lb_cost:
                # Early stop condition
                if s2_cost <= ub_cost and early_stop:
                    return s2, s2_cost, bests, cost_iterator
                # Cải tiến cục bộ nghiệm tốt hơn đó
                LocalSearch.local_search_v2(s2, r_le2, r_c2, distance_matrix)
                # Tính toán lại cost sau khi thực hiện local search
                ls_cost, ls_regularize = np.sum(r_c2), penalty_s1(x, y, s2, r_le2, alpha)

                # Chấp nhận nghiệm mới được sinh ra (trong trường hợp có early stop thì sẽ chỉ chấp nhận nếu > lower bound)
                if ls_cost >= lb_cost:
                    solution, route_length, route_costs, route_load = np.copy(s2), np.copy(r_le2), np.copy(r_c2), np.copy(r_lo2)
                    cur_cost, cur_reg = ls_cost, ls_regularize
                    if ls_cost <= ub_cost and early_stop:
                        return solution, ls_cost, bests, cost_iterator
                else:
                    # Nếu vi phạm lower bound, loại bỏ nghiệm local search và không tính là nghiệm tốt nhất tìm được
                    ls_cost = 9999999

                # Cơ chế tính điểm và cập nhật nghiệm tốt nhất tìm được
                # Nếu nghiệm mới còn tốt hơn nghiệm tốt nhất tìm được (nếu ls < lower thì sẽ không xảy ra trường hợp này)
                if ls_cost + ls_regularize < best_cost + best_reg_cost:
                    if log:
                        print("ITERATION", i, ": Cost =", ls_cost, "\tRegularize =", ls_cost + ls_regularize)
                    test = 0
                    # Cập nhật nghiệm tốt nhất
                    best_sol, best_cost, best_reg_cost = np.copy(s2), ls_cost, ls_regularize
                    # Cập nhật điểm dựa trên performance (PHI_1 > PHI_2 > PHI_3 > 0)
                    AdaptiveMechanism.update_score(operators, Config.PHI_1, destroy_score,
                                                   destroy_used, repair_score, repair_used)
                else:
                    AdaptiveMechanism.update_score(operators, Config.PHI_2, destroy_score,
                                                   destroy_used, repair_score, repair_used)
            else:
                AdaptiveMechanism.update_score(operators, Config.PHI_3, destroy_score, destroy_used,
                                               repair_score, repair_used)

            # Co che chap nhan nghiem dang duoc thu nghiem (Inspire tu thuat toan Record-to-Record)
            if s2_cost + s2_regularize < best_cost + best_reg_cost + Config.DEVIATION:
                solution, route_length, route_costs, route_load = np.copy(s2), np.copy(r_le2), np.copy(r_c2), np.copy(r_lo2)
                cur_cost, cur_reg = s2_cost, s2_regularize

            # Considering very good effect (+150 for 2k total cost) (+100 for n39k6). Co time thi phat trien
            if test >= 1000 and s2_cost <= best_cost + Config.BIG_DEVIATION:
                solution, route_length, route_costs, route_load = np.copy(s2), np.copy(r_le2), np.copy(r_c2), np.copy(r_lo2)
                cur_cost, cur_reg = s2_cost, s2_regularize
                test = 0
        else:
            # Xử lý nếu nghiệm không thể sửa được
            removed.fill(0)
            AdaptiveMechanism.update_score(operators, Config.PHI_3, destroy_score, destroy_used, repair_score, repair_used)

        # Vao dau moi segment, cap nhat trong so cac operator va tien hanh Local Search len nghiem hien tai
        if (i + 1) % ips == 0:
            AdaptiveMechanism.update_weight(destroy_operator, destroy_weight, destroy_score, destroy_used,
                                            repair_operator, repair_weight, repair_score, repair_used)

            # Case nay co the violate khi early stop nen tot nhat la khong cho
            if not early_stop:
                LocalSearch.local_search_v2(solution, route_length, route_costs, distance_matrix)
                ls_cost, ls_regularize = np.sum(route_costs), penalty_s1(x, y, s2, r_le2, alpha)
                if ls_cost + ls_regularize < best_cost + best_reg_cost:
                    best_sol, best_cost, best_reg_cost = np.copy(solution), ls_cost, ls_regularize



        # Lấy mốc thời gian ra
        if time_it < len(bests):
            with objmode(end_time='float64'):
                end_time = time.process_time()

            if end_time - start_time >= 0.01:
                start_time = end_time
                bests[time_it] = best_cost
                time_it += 1
        else:
            # Vì đang test operator neên hard-code dừng thuật toán sớm
            return best_sol, best_cost, bests, cost_iterator

    # Khi tìm xong, in ra và trả về nghiệm tốt nhất tìm được
    if log:
        print()
        print("Best cost:", best_cost)
        print(best_sol)
    return best_sol, best_cost, bests, cost_iterator




