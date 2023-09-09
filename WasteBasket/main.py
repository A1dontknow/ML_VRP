"""
This file currently do nothing
"""
import os
import random
import time

import numpy as np

from Instances.Features import Features
from Instances.Instance import Instance
from Instances.Solution import Solution
from Visual import visualize
from numba import njit
from numba.typed import Dict, List
import numba

def test_feature():
    project_path = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(project_path + "\Dataset\Instance\\")
    instances = [f.split(".")[0] for f in files if f.endswith('.txt')]

    ok = 0
    for i in range(len(instances)):
        chosen_one = instances[i]
        ins = Instance(chosen_one)
        opt_sol = Solution(chosen_one + "_opt.txt", ins)
        nopt_sol = Solution(chosen_one + "_nopt.txt", ins)
        opt_f = Features(ins, opt_sol)
        nopt_f = Features(ins, nopt_sol)
        if opt_f.get_experimental()[0] < nopt_f.get_experimental()[0]:
            ok += 1
        print("Passed %d / %d" % (ok, i))

# Some function to play with numba for fun
@njit(cache=True)
def count_set(input_list):
    unique_set = set(input_list)
    return len(unique_set)


@njit(cache=True)
def count_unique(input_list):
    input_list.sort()
    uni = 1
    current_number = input_list[0]
    for i in range(1, len(input_list)):
        if current_number != input_list[i]:
            uni += 1
            current_number = input_list[i]
    return uni


if __name__ == "__main__":
    # a = List([random.randint(1, 2000000) for i in range(2000000)])
    # print("n =", len(a))
    # t1 = time.process_time()
    # print("Number of unique element using set:", count_set(a))
    # t2 = time.process_time()
    # print("Number of unique element by sorting: ", count_unique(a))
    # t3 = time.process_time()
    # print("\nSet time =", t2 - t1)
    # print("\nSort time =", t3 - t2)
    # test_feature()

    # project_path = os.path.dirname(os.path.abspath(__file__))
    # files = os.listdir(project_path + "\Dataset\Instance\\")
    # instances = [f.split(".")[0] for f in files if f.endswith('.txt')]
    # chosen_one = random.choice(instances)
    # ins = Instance(chosen_one)
    # opt_sol = Solution(chosen_one + "_opt.txt", ins)
    # nopt_sol = Solution(chosen_one + "_nopt.txt", ins)
    # opt_f = Features(ins, opt_sol)
    # nopt_f = Features(ins, nopt_sol)
    # print(opt_f.get_experimental()[0], nopt_f.get_experimental()[0])
    # visualize(chosen_one)

    # print("Experimental feature for optimal sol:", opt_f.get_experimental())
    # print("Experimental feature for non-optimal sol:", nopt_f.get_experimental())

    project_path = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(project_path + "\Dataset\Instance\\")
    instances = [f.split(".")[0] for f in files if f.endswith('.txt')]
    instance_10000_plus = [i for i in instances if len(i) >= 13]
    a = instance_10000_plus[10001:15001]
    b = instance_10000_plus[15001:20001]
    c = instance_10000_plus[1:10001]
    # print(c[10000])
    print(a)
    # print(b)
    d = [i for i in instances if len(i) < 13]
    d.append(instance_10000_plus[0])
    print(len(a), len(b), len(c), len(d))
    print(a)
