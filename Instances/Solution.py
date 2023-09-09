import re


class Solution:
    """
    :param routes: Cac tuyen xe
    :param instance: Mo ta cua bai toan

    Ham xay dung loi giai bao gom:
        - instance (Instance): Mo ta bai toan
        - routes (list): Danh sach cac tuyen xe
    """
    def __init__(self, file_name, instance):
        self.instance = instance
        self.routes = []
        self.cost = -1
        self.read_solution(file_name)

    def read_solution(self, file_name):
        try:
            f = None
            try:
                f = open("C:\\Users\\Dell\\PycharmProjects\\pythonProject2\\Dataset\\Solution\\ALNS\\" + file_name)
            except FileNotFoundError:
                try:
                    f = open("C:\\Users\\Dell\\PycharmProjects\\pythonProject2\\Dataset\\Solution\\ALNS\\" + file_name + ".txt")
                except FileNotFoundError:
                    print("Ten Solution khong dung")
                    exit(-1)

            self.cost = float(f.readline().strip().split(" ")[-1])
            line = f.readline()
            while line:
                route = []
                nums = [int(i) for i in re.findall(r'\d+\.*\d*', line)]
                route.append(self.instance.depot)
                for i in range(2, len(nums) - 1):
                    route.append(self.instance.customers[nums[i] - 1])
                route.append(self.instance.depot)
                if len(route) > 2:
                    self.routes.append(route)
                line = f.readline()

            f.close()
        except Exception:
            print("Loi nhap du lieu: Solution khong khop dinh dang")
            exit(-1)

    def __str__(self):
        return f'Solution: Total cost = {"%.2f" %self.cost}, Routes = \n{self.routes})'

