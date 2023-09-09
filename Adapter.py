import multiprocessing
import os
import re

from Solver import Config
from Solver.Adapter import get_solution

"""
    Ket noi Solver cua ALNS de sinh ra solution set. Parameter hoi fix cung' mot chut
    Sinh ra near-optimal solution, thay tham so optimal tat ca ham = True, nguoc lai set = False
"""

def solve_optimal_alns(instance_name, optimal=True, min_gap=0.03, max_gap=0.05, known_optimal=False):
    Config.PRINT_LOG = 0
    Config.PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    customers = re.findall(r'\d+\.*\d*', instance_name)[0]

    if not optimal:
        Config.EARLY_STOP = 1
        Config.MIN_GAP = min_gap
        Config.MAX_GAP = max_gap
        if not known_optimal:
            try:
                f = open(os.path.dirname(os.path.abspath(__file__)) + "\Dataset\Solution\ALNS_string\\" + instance_name + "_opt.txt")
                Config.OPTIMAL = float(f.readline().strip().split(" ")[-1])
                f.close()
            except FileNotFoundError:
                print("Khong tim thay du lieu lien quan den optimal cost")
                exit(-1)

    if int(customers) > 60:
        Config.ITERATION = 3000000
        Config.SEGMENT = 30000
    else:
        Config.ITERATION = 1000000
        Config.SEGMENT = 10000

    sol, cost = get_solution(instance_name)

    if optimal:
        file_path = os.path.dirname(os.path.abspath(__file__)) + "\Dataset\Solution\ALNS_string\\" + instance_name + "_opt.txt"
    else:
        file_path = os.path.dirname(os.path.abspath(__file__)) + "\Dataset\Solution\ALNS_string\\" + instance_name + "_nopt.txt"
    try:
        with open(file_path, 'w') as f:
            # Write some text to the file
            f.write("Best cost: " + str(cost) + "\n")
            for i in range(len(sol)):
                f.write("Route #" + str(i + 1) + ": [0, ")
                j = 1
                while sol[i][j] != 0:
                    f.write(str(sol[i][j]) + ", ")
                    j += 1
                f.write("0]\n")
    except:
        os.remove(file_path)
            

def multi_solve_alns():
    project_path = os.path.dirname(os.path.abspath(__file__))
    # Lay toan bo file trong thu muc dataset
    files = os.listdir(project_path + "\Dataset\\")
    instance = [f.split(".")[0] for f in files if f.endswith('.txt')]
    print("There are total of", len(instance), "instances")
    print("Begin to solve:")
    for i in range(len(instance)):
        solve_optimal_alns(instance[i])
        print("Solved " + str(i + 1) + "/" + str(len(instance)))
    print()
    print("Finished")


def multi_parallel_solve_alns(num_cpu=8, optimal=True):
    project_path = os.path.dirname(os.path.abspath(__file__))
    # Lay toan bo file trong thu muc dataset
    files = os.listdir(project_path + "\Dataset\\Instance\\")
    instance = [f.split(".")[0] for f in files if f.endswith('.txt')]

    # Tìm những file chưa được solve
    unsolved = []
    for f in instance:
        if optimal:
            if not os.path.exists(project_path + "\Dataset\Solution\ALNS_string\\" + f + "_opt.txt"):
                unsolved.append(f)
        else:
            if not os.path.exists(project_path + "\Dataset\Solution\ALNS_string\\" + f + "_nopt.txt"):
                unsolved.append(f)
    print(unsolved)

    print("Begin to solve in parallel:")

    pool = multiprocessing.Pool(processes=num_cpu)
    pool.map(solve_optimal_alns, unsolved)
    pool.close()
    pool.join()


if __name__ == "__main__":
    multi_parallel_solve_alns()
    # project_path = os.path.dirname(os.path.abspath(__file__))
    # files = os.listdir(project_path + "\Dataset\\Instance\\")
    # instance = [f.split(".")[0] for f in files if f.endswith('.txt')]

    # Tìm những file chưa được solve
    # oldsolved = ['I11101-n25-k5', 'I12764-n28-k3', 'I13079-n26-k3', 'I13380-n28-k3', 'I15096-n20-k5', 'I15510-n25-k5', 'I17659-n36-k6', 'I18123-n27-k5', 'I19005-n31-k6', 'I19689-n22-k4', 'I2271-n25-k5', 'I2294-n26-k6', 'I3233-n29-k6', 'I3294-n22-k5', 'I3394-n29-k5', 'I4016-n31-k3', 'I4098-n21-k6', 'I6358-n30-k6', 'I6410-n27-k5', 'I7482-n41-k6', 'I7845-n25-k5', 'I9668-n31-k6']
    # unsolved = []
    # #
    # for instance_name in instance:
    #     f = open(project_path + "\Dataset\Solution\ALNS\\" + instance_name + "_nopt.txt")
    #     if float(f.readline().strip().split(" ")[-1]) == -1:
    #         unsolved.append(instance_name)
    #     f.close()
    #
    # print(unsolved)
    # pool = multiprocessing.Pool(processes=7)
    # pool.map(solve_optimal_alns, oldsolved)
    # pool.close()
    # pool.join()

