import math

import numpy as np
import re
from Instances.Node import Node


class Instance:
    """
    :param file_name: File bai toan de giai

    Ham nay de dung cac thuoc tinh cho bai toan
        - optimal (float): Gia tri toi uu biet truoc
        - vehicles (int): So xe
        - capacity (int): Tai trong cua xe
        - dimensions (int): So luong khach hang (= so luong yeu cau)
        - customers (list Node): Thong tin cua cac khach hang
        - depot (Node): Diem lay hang cua moi xe
        - distance_matrix (2D float): Ma tran khoang cach giua cac khach hang va kho voi nhau
    """
    def __init__(self, file_name):
        self.optimal = None
        self.vehicles = None
        self.capacity = None
        self.dimensions = 0
        # Customers are mapped with nodes
        self.customers = []
        self.depot = None
        self.distance_matrix = []
        self.load_data(file_name)
        self.create_distance_matrix_v2()

    def load_data(self, file_name):
        try:
            f = None
            try:
                f = open("C:\\Users\\Dell\\PycharmProjects\\pythonProject2\\Dataset\\Instance\\" + file_name)
            except FileNotFoundError:
                try:
                    f = open("C:\\Users\\Dell\\PycharmProjects\\pythonProject2\\Dataset\\Instance\\" + file_name + ".txt")
                except FileNotFoundError:
                    print("Ten instance khong dung")
                    exit(-1)

            lines = f.readlines()
            line_two = re.findall(r'\d+',lines[1])
            # # Input binh thuong co the khong co thong tin ve optimal
            # try:
            #     self.optimal = int(line_two[1])
            # except Exception:
            #     self.optimal = -1
            self.vehicles = int(line_two[0])
            self.dimensions = int(re.findall(r'\d+', lines[3])[0])
            self.capacity = int(re.findall(r'\d+', lines[5])[0])

            # Tu dong 8 lay thong tin vi tri kho, khach hang va nhu cau cua khach
            for i in range(self.dimensions):
                demand = int(lines[8 + self.dimensions + i].split().pop())
                node = lines[7 + i].split()
                y = node.pop()
                x = node.pop()
                # Truong hop kho. Gia su rang kho se co demand = 0
                if demand == 0:
                    self.depot = Node(i, x, y, demand)
                else:
                    self.customers.append(Node(i, x, y, demand))
        except Exception:
            print("Loi nhap du lieu: Instance khong khop dinh dang")
            exit(-1)

    # Tao ma tran khoang cach giua khach hang va depot voi nhau (Old ngáo implementation)
    def create_distance_matrix(self):
        nodes = [self.depot] + self.customers
        for i in range(len(nodes)):
            row = []
            for j in range(len(nodes)):
                if i == j:
                    row.append(0)
                else:
                    vector = np.array([nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y])
                    row.append(np.linalg.norm(vector))
            self.distance_matrix.append(row)
        self.distance_matrix = np.array(self.distance_matrix)

    def create_distance_matrix_v2(self):
        nodes = [self.depot] + self.customers
        self.distance_matrix = np.zeros((len(nodes), len(nodes)))
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                self.distance_matrix[i][j] = math.sqrt((nodes[i].x - nodes[j].x) ** 2 + (nodes[i].y - nodes[j].y) ** 2)

