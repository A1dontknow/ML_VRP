import os
from Instances.Features import Features
from Instances.Instance import Instance
from Instances.Solution import Solution


# Convert toan bo file trong Instance
def convert():
    project_path = os.path.dirname(os.path.abspath(__file__))
    # Lay toan bo file trong thu muc dataset
    files = os.listdir(project_path + "\Dataset\Instance\\")
    instances = [f.split(".")[0] for f in files if f.endswith('.txt')]

    file_path = project_path + "\Dataset\MLData\CVRP_true.txt"

    try:
        with open(file_path, 'w') as f:
            for i in range(len(instances)):
                print(i)
                instance = instances[i]
                ins = Instance(instance)
                sol = Solution(instance + "_opt.txt", ins)
                sol2 = Solution(instance + "_nopt.txt", ins)
                f_opt = [round(i, 6) for i in Features(ins, sol).to_feature()]
                f_nopt = [round(i, 6) for i in Features(ins, sol2).to_feature()]
                f_opt.insert(0, 1)
                f_nopt.insert(0, 0)

                f_nopt_str = str(f_nopt)
                f_opt_str = str(f_opt)
                f.write(f_nopt_str[1:len(f_nopt_str) - 1] + "\n")
                f.write(f_opt_str[1:len(f_opt_str) - 1] + "\n")
    except:
        # print("he")
        os.remove(file_path)


# Convert data includes 2000 data points of instance n > 70
def convert_mini():
    project_path = os.path.dirname(os.path.abspath(__file__))
    # Lay toan bo file trong thu muc dataset
    files = os.listdir(project_path + "\Dataset\Instance\\")
    instances = [f.split(".")[0] for f in files if f.endswith('.txt')]
    big_instances = [f for f in instances if len(f) == 13][10001:12002]
    print(big_instances)
    print(len(big_instances))
    file_path = project_path + "\Dataset\MLData\CVRP_N_2000.txt"

    try:
        with open(file_path, 'w') as f:
            for i in range(len(big_instances)):
                print(i)
                instance = big_instances[i]
                ins = Instance(instance)
                sol = Solution(instance + "_opt.txt", ins)
                sol2 = Solution(instance + "_nopt.txt", ins)
                f_opt = [round(i, 6) for i in Features(ins, sol).to_feature()]
                f_nopt = [round(i, 6) for i in Features(ins, sol2).to_feature()]
                f_opt.insert(0, 1)
                f_nopt.insert(0, 0)

                f_nopt_str = str(f_nopt)
                f_opt_str = str(f_opt)
                f.write(f_nopt_str[1:len(f_nopt_str) - 1] + "\n")
                f.write(f_opt_str[1:len(f_opt_str) - 1] + "\n")
    except:
        # print("he")
        os.remove(file_path)


if __name__ == "__main__":
    convert()
    # convert_mini()