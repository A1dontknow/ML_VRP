import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from Instances.Features import Features
from Instances.Instance import Instance
from Instances.Solution import Solution

"""
    File visual solution
"""

# Support ham visualize()
def plot_solution(ins, sol, fig, ax, is_optimal=True):
    f = Features(ins, sol)
    for i in range(len(sol.routes)):
        x = []
        y = []
        for node in sol.routes[i]:
            x.append(node.x)
            y.append(node.y)
        ax.plot(x, y, label="Route " + str(i + 1))
        ax.plot(x, y, 'or')

    ax.plot(sol.routes[0][0].x, sol.routes[0][0].y, "sk", label="Depot")

    Gr = f.Gr
    x_g = [i[0] for i in Gr]
    y_g = [i[1] for i in Gr]
    # ax.plot(x_g, y_g, "ok", label="Gravity")
    if is_optimal:
        ax.set_title("CVRP near-optimal cost = %f" % sol.cost)
    else:
        ax.set_title("CVRP non-optimal cost = %f" % sol.cost)
    ax.legend()


# Ve solution optiomal va non-optimal cua mot instance
def visualize(instance_name):
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    ins = Instance(instance_name)
    opt_sol = Solution(instance_name + "_opt.txt", ins)
    nopt_sol = Solution(instance_name + "_nopt.txt", ins)
    plot_solution(ins, opt_sol, fig1, ax1)
    plot_solution(ins, nopt_sol, fig2, ax2, is_optimal=False)

    plt.show()


# Ve solution ra cua mot instance
def plot_custom(ins, sol):
    f = Features(ins, sol)
    for i in range(len(sol.routes)):
        x = []
        y = []
        for node in sol.routes[i]:
            x.append(node.x)
            y.append(node.y)
        plt.plot(x, y, label="Route " + str(i + 1))
        plt.plot(x, y, 'or')
    print(f.to_feature())
    plt.plot(sol.routes[0][0].x, sol.routes[0][0].y, "sk", label="Depot")

    Gr = f.Gr
    x_g = [i[0] for i in Gr]
    y_g = [i[1] for i in Gr]
    plt.plot(x_g, y_g, "ok")
    # ax.plot(x_g, y_g, "ok", label="Gravity")
    plt.title("CVRP near-optimal cost = %f" % sol.cost)
    plt.show()


# Visualize data trong MLData da duoc trich xuat dac trung
def visual_data_PCA(data_path, n_components=2):
    f = open(data_path)
    data = np.genfromtxt(f, delimiter=',')
    X = data[:, 1:len(data[0])]
    y = np.array(data[:, 0], dtype=np.int32)

    # Standardize the feature data
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    if n_components != 2 and n_components != 3:
        n_components = 2

    # Apply PCA 2D
    if n_components == 2:
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_std)

        # Visualize the transformed data
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y)
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.show()

    # Apply PCA with 3 components
    elif n_components == 3:
        pca = PCA(n_components=3)
        X_pca = pca.fit_transform(X_std)

        # Visualize the transformed data in 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=y)
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
        plt.show()


if __name__ == "__main__":
    # visual_data_PCA("C:\\Users\Dell\PycharmProjects\pythonProject2\Dataset\MLData\CVRP_test.txt", 2)
    visualize("I27828-n100-k10")
    # visualize("I60-n50-k5")
    # ins = Instance("A.txt")
    # sol = Solution("A.txt", ins)
    # plot_custom(ins, sol)