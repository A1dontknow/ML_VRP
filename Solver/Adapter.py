import numpy as np
from matplotlib import pyplot as plt

from Solver import Config
from Solver.Algorithm.ALNS import solve_v2
from Solver.Instances.Instance import load_data


def solve_and_visual(data_name):
    Config.PROJECT_PATH = "C:\\Users\Dell\PycharmProjects\pythonProject2\\"
    Config.ITERATION = 1000000
    Config.SEGMENT = 10000
    Config.alpha = 0
    #
    # Config.PRINT_LOG = 0
    optimal, vehicles, capacity, demand, x, y, distance_matrix = load_data(data_name)
    best, cost, bests, _ = solve_v2(x, y, vehicles, capacity, demand, distance_matrix, True)

    # Testing stuff
    confirm_cost = 0
    for r in best:
        confirm_cost += distance_matrix[r[0]][r[1]]
        i = 1
        while r[i] != 0:
            confirm_cost += distance_matrix[r[i]][r[i + 1]]
            i += 1
    print("True cost =", confirm_cost)
    cost = confirm_cost

    for route in best:
        a = []
        b = []
        z = 0
        for node in route:
            if node == 0:
                z += 1
            a.append(x[node])
            b.append(y[node])
            if z == 2:
                break

        plt.plot(a, b)
        plt.plot(a, b, 'or')
        plt.plot(x[0], y[0], "sk")
    plt.title("VRP Solution (Cost = " + str("%.2f" % cost) + ")")

    plt.show()


def get_solution(instance_name):
    optimal, vehicles, capacity, demand, x, y, distance_matrix = load_data(instance_name)
    print(instance_name)
    best, cost = solve_v2(x, y, vehicles, capacity, demand, distance_matrix)
    return best, cost


def operator_experiment(instance_name):
    Config.PROJECT_PATH = "C:\\Users\Dell\PycharmProjects\pythonProject2\\"
    # Config.ITERATION = 100000
    # Config.SEGMENT = 1000
    Config.PRINT_LOG = 0

    # iteration = np.arange(100000) + 1
    time = np.linspace(0, 2, 201).round(3)
    optimal, vehicles, capacity, demand, x, y, distance_matrix = load_data(instance_name)
    old = np.zeros(201)
    new = np.zeros(201)
    for i in range(50):
        print(i)
        _, _, test_old, _ = solve_v2(x, y, vehicles, capacity, demand, distance_matrix, False)
        _, _, test_new, _ = solve_v2(x, y, vehicles, capacity, demand, distance_matrix, True)
        print(test_old)
        old += test_old
        new += test_new

    print(new / 50)

    # 826.91 = true known optimal E-n101-k8 CVRPLIB
    old = old / (50 * 826.91) * 100 - 100
    new = new / (50 * 826.91) * 100 - 100
    plt.plot(time, old, label="Worst Destroy")
    plt.plot(time, new, label="Intersect Destroy")
    plt.legend()
    plt.title("Average gap over time")
    plt.xlabel("Time (s)")
    plt.ylabel("Gap (%)")
    plt.show()


# Kiểm tra early stop hoạt động ổn không
if __name__ == "__main__":
    # operator_experiment("E-n101-k8")
    solve_and_visual("E-n101-k8")
    # Config.EARLY_STOP = 1
    # Config.PRINT_LOG = 0
    # Config.OPTIMAL = 6196.010133388283
    # Config.MIN_GAP = 0.03
    # Config.MAX_GAP= 0.05


