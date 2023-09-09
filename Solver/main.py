from Solver.Algorithm.ALNS import solve_v2
from Solver.Instances.Instance import load_data
import matplotlib.pyplot as plt
import time
import Solver.Config as Config
import os


def main():
    Config.PROJECT_PATH = "C:\\Users\Dell\PycharmProjects\pythonProject2\\"
    print("ALNS for Vehicle Routing Problem")
    print("--------------------------------")
    print("Ban hay nhap ten file trong thu muc CVRP\\Dataset de giai.\nLuu y: File ban can giai can "
          "co dinh dang khop voi cac file trong thu muc <ProjectPath>\\CVRP\\Dataset\\. Vi du: \"A-n36-k5\"")
    file = input()
    # Khoi tao instance cho bai toan
    optimal, vehicles, capacity, demand, x, y, distance_matrix = load_data(file)
    print("----------------------------------------------------")

    # Dung ALNS de solve
    # best, cost = solve_v2(x, y, vehicles, capacity, demand, distance_matrix)
    # Best of A-n32-k5 from CVRPLIB
    # best = [[0, 21, 31, 19, 17, 13, 7, 26, 0],[0, 12, 1, 16, 30, 0],[0, 27, 24, 0],[0, 29, 18, 8, 9, 22, 15, 10, 25, 5, 20, 0],[0, 14, 28, 11, 4, 23, 3, 2, 6, 0]]
    # Best of E-n101-k8 from CVRPLIB
    best = [[0, 28, 12, 80, 68, 29, 24, 54, 55, 25, 4, 26, 53, 0], [0, 92, 37, 98, 100, 91, 16, 86, 44, 38, 14, 42, 43, 15, 57, 2, 58, 0], [0, 27, 69, 1, 70, 30, 20, 66, 32, 90, 63, 10, 62, 88, 31, 0], [0, 6, 96, 99, 59, 93, 85, 61, 17, 45, 84, 5, 60, 89, 0], [0, 52, 7, 82, 48, 19, 11, 64, 49, 36, 47, 46, 8, 83, 18, 0], [0, 73, 74, 22, 41, 23, 67, 39, 56, 75, 72, 21, 40, 0], [0, 13, 87, 97, 95, 94, 0], [0, 50, 33, 81, 51, 9, 71, 65, 35, 34, 78, 79, 3, 77, 76, 0]]
 #    best = [[ 0, 18, 22, 12, 57, 11, 15, 0],
 #            [ 0, 10, 56, 52, 13, 61, 24, 32, 42, 0],
 #            [ 0, 23, 37, 31, 50, 36, 40, 39, 44,  7, 21, 26, 35, 30,  0],[ 0, 17,  1, 27, 14, 28, 43, 38,  0],
 # [ 0,  9, 54, 58,  2, 63, 47, 46,  8, 16, 60, 41,  0],
 # [ 0, 34,  4,  5, 59, 55, 49, 53,  0],
 # [ 0, 45,  3, 51, 19, 20,  0],
 # [ 0, 33, 62, 48,  0],
 # [ 0, 25, 29,  6,  0]]
    # Testing stuff
    confirm_cost = 0
    for r in best:
        confirm_cost += distance_matrix[r[0]][r[1]]
        i = 1
        while r[i] != 0:
            confirm_cost += distance_matrix[r[i]][r[i+1]]
            i += 1
    print("True cost =", confirm_cost)
    cost = confirm_cost

    # Luu nghiem tot nhat vao file
    t = time.localtime()
    current_time = time.strftime("%H_%M_%S", t)
    if not os.path.exists(Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0]):
        os.mkdir(Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0])
    f = open(Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0] + "\\" + current_time + ".txt",
             "wt")
    f.write(str(cost))
    f.write(str(best))
    f.close()

    # Minh hoa bang matplotlib va save anh
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
    plt.savefig(
        Config.PROJECT_PATH + "\\Dataset\\Solution\\" + file.split(".txt")[0] + "\\" + current_time + ".png")
    print("Anh va file da duoc luu vao trong thu muc <ProjectPath>\\CVRP\\Dataset\\Solution\\<Ten file>\\")
    plt.show()


if __name__ == '__main__':
    main()
