import numpy as np

from Math_support import *


class Features:
    """
        Lớp thực hiện xây dựng các đặc trưng (S1-S10) để phân loại một nghiệm có tốt hay không:
        Reference: https://www.sciencedirect.com/science/article/abs/pii/S0305054818300315
    """
    def __init__(self, instance, solution):
        self.distance_matrix = instance.distance_matrix
        self.routes = solution.routes
        self.N = instance.dimensions - 1
        self.R = len(self.routes)
        # Gr (list): Gravity của route r đc lưu = list tọa độ (x, y)
        self.Gr = self.calculate_Gr()
        self.lazy_load = False


    def calculate_Gr(self):
        Gr = []
        for r in self.routes:
            x = 0
            y = 0
            r_length = len(r) - 1       # A route count depot only once
            for i in range(r_length):
                x += r[i].x
                y += r[i].y
            Gr.append((x / r_length, y / r_length))
        return Gr

    def calculate_S1(self):
        s1 = 0
        for i in range(self.R - 1):
            for j in range(i + 1, self.R):
                intersect = I(self.routes[i], self.routes[j])
                if intersect > 0:
                    # print(i, j, ":", intersect)
                    s1 += intersect
        return s1 / self.N

    def calculate_S2(self):
        s2 = 0
        for r in self.routes:
            max_dis = 0
            for i in range(1, len(r) - 2):
                if self.distance_matrix[r[i].id][r[i + 1].id] > max_dis:
                    max_dis = self.distance_matrix[r[i].id][r[i + 1].id]
            s2 += max_dis
        return s2 / self.R

    def calculate_S3(self):
        s3 = 0
        for r in self.routes:
            # r = [0, a, b, c, 0]   (a, b, c in N)
            s3 += self.distance_matrix[r[0].id][r[1].id] + self.distance_matrix[r[-1].id][r[-2].id]
        return s3 / (2 * self.R)

    def calculate_S4(self):
        s4 = 0
        for i in range(self.R):
            for j in range(self.R):
                if i != j:
                    x1, y1 = self.Gr[i]
                    x2, y2 = self.Gr[j]
                    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                    s4 += distance
        return s4 / (self.R * (self.R - 1))


    def calculate_S5(self):
        s5 = 0
        for r in range(len(self.routes)):
            min_d = 9999999
            max_d = 0
            for i in range(1, len(self.routes[r]) - 1):
                x1, y1 = self.routes[r][i].x, self.routes[r][i].y
                x2, y2 = self.Gr[r]
                distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if min_d > distance:
                    min_d = distance
                if max_d < distance:
                    max_d = distance
            # Thử cộng, not trừ như trong bài báo
            # if min_d == 9999999:
            #     print("oh no")
            s5 += (max_d - min_d)
        return s5 / self.R


    # def calculate_S5(self):
    #     s5 = 0
    #     for r in range(len(self.routes)):
    #         s5 += avg_width_route(self.routes[r], self.Gr[r])
    #     return s5 / self.R

    def calculate_S6(self):
        s6 = 0
        for r in self.routes:
            max_rad = 0
            for i in range(1, len(r) - 2):
                for j in range(i + 1, len(r) - 1):
                    if i != j:
                        angle = rad(r[i].xy, r[j].xy, r[0].xy)  # r[0] is depot
                        if angle > max_rad:
                            max_rad = angle
            s6 += max_rad
        return s6 / self.R

    def calculate_S7(self):
        s7 = 0
        for r in range(len(self.routes)):
            for i in range(1, len(self.routes[r]) - 1):
                x1, y1 = self.routes[r][i].x, self.routes[r][i].y
                x2, y2 = self.Gr[r]
                distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                s7 += distance
        return s7 / self.N

    def calculate_S8(self):
        s8 = 0
        x_d, y_d = self.routes[0][0].xy
        for r in range(len(self.routes)):
            for i in range(1, len(self.routes[r]) - 1):
                x1, y1 = self.routes[r][i].x, self.routes[r][i].y
                x2, y2 = self.Gr[r]
                angle = rad((x1, y1), (x2, y2), (x_d, y_d))
                s8 += angle
        return s8 / self.N

    def calculate_S9(self):
        s9 = 0
        D = self.routes[0][0]
        for r in self.routes:
            max_d = 0
            for n in r:
                distance = self.distance_matrix[n.id][D.id]
                if distance > max_d:
                    max_d = distance
            s9 += max_d
        return s9 / self.R

    def calculate_S10(self):
        s10 = 0
        for r in self.routes:
            s10 += ((len(r) - 2) - self.N / self.R) ** 2         # len(r) - 2 vì chỉ lấy số customer
        return math.sqrt(s10 / self.R)

    def to_feature(self):
        if not self.lazy_load:
            # Average number of intersections per customer
            self.S1 = self.calculate_S1()
            # Longest distance between two connected customers, per route
            self.S2 = self.calculate_S2()
            # Average distance between depot to directly-connected customer
            self.S3 = self.calculate_S3()
            # Average distance between routes (their centers of gravity)
            self.S4 = self.calculate_S4()
            # Average width per route
            self.S5 = self.calculate_S5()
            # Average span in radian per route
            self.S6 = self.calculate_S6()
            #  Average compactness per route, measured by width
            self.S7 = self.calculate_S7()
            # Average compactness per route, measured by radian
            self.S8 = self.calculate_S8()
            # Average depth per route
            self.S9 = self.calculate_S9()
            # Standard deviation of the number of customers per route
            self.S10 = self.calculate_S10()
            self.lazy_load = True
        return [self.S1, self.S2, self.S3, self.S4, self.S5, self.S6, self.S7, self.S8, self.S9, self.S10]#, self.calculate_E1(), self.calculate_E4()]


    # Below is some personal experimental stuff
    def get_experimental(self):
        self.test1 = self.calculate_E4()
        # Bone-fish ratio?
        # self.E = self.calculate_S2()
        return [self.test1]



    def calculate_E1(self):
        e1 = 0
        for r in self.routes:
            f = max(r, key= lambda x : self.distance_matrix[0][x.id])
            Of = self.distance_matrix[0][f.id]
            max_fish = 0
            for x in range(1, len(r) - 1):
                Ox = self.distance_matrix[0][r[x].id]
                xy = self.distance_matrix[r[x].id][r[x + 1].id]
                fish_bone = (Ox + xy - Of) / Of
                if fish_bone > max_fish:
                    max_fish = fish_bone
            e1 += max_fish ** 2
        return e1



    def calculate_E2(self):
        e2 = 0
        for r in self.routes:
            f = max(r, key= lambda x : self.distance_matrix[0][x.id])
            Of = self.distance_matrix[0][f.id]
            max_fish = 0
            for x in range(1, len(r) - 1):
                Ox = self.distance_matrix[0][r[x].id]
                xy = self.distance_matrix[r[x].id][r[x + 1].id]
                fish_bone = (Ox + xy - Of) / Of
                if fish_bone > max_fish:
                    max_fish = fish_bone
            e2 += max_fish
        return e2



    def calculate_E3(self):
        max_fish = np.zeros(len(self.routes))
        i = 0
        for r in self.routes:
            f = max(r, key= lambda x : self.distance_matrix[0][x.id])
            Of = self.distance_matrix[0][f.id]

            for x in range(1, len(r) - 1):
                Ox = self.distance_matrix[0][r[x].id]
                xy = self.distance_matrix[r[x].id][r[x + 1].id]
                fish_bone = (Ox + xy - Of) / Of
                if fish_bone > max_fish[i]:
                    max_fish[i] = fish_bone

            i += 1

        return np.std(max_fish)


    # Dont know how to get a name. Route cost / spider?
    def calculate_E4(self):
        e4 = 0
        for r in self.routes:
            cost = 0
            link_spider = 0
            for customer in range(len(r) - 1):
                cost += self.distance_matrix[r[customer].id][r[customer + 1].id]
                link_spider += self.distance_matrix[0][r[customer].id]
            e4 += cost / link_spider
        return e4