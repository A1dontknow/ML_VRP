import os
import random


def gen_instance(no_instance):
    """
    Hàm phục vụ việc sinh bộ dữ liệu:
        - Tọa độ: Ngẫu nhiên trên tọa độ 1000 x 1000
        - Số lượng khách hàng: 20 - 50 OR 70 - 100 (ratio 1:2)
        - Demand: Variance in [0, 10]
        - Số xe: 3 - 6 (20 - 50)
                6 - 10 (70 - 100)
    :return:
    """
    data_path = os.path.dirname(os.path.abspath(__file__)) + "\\Dataset\\"
    # Phòng việc bấm nhầm dữ liệu bị gen lại
    data = [f for f in os.listdir(data_path) if f.endswith('.txt')]
    if len(data) >= 100:
        print("Dataset đã có sẵn. Hãy xóa thủ công rồi chạy lại")

    gen_ed = 0
    no_customer = -1        # no_customer đã bao gồm depot để đồng nhất format CVRPLIB
    demand_variance = -1
    no_trucks = -1
    tight = -1
    ins_name = "???"
    while gen_ed < no_instance:
        # Khởi tạo giá trị cho instance được gen
        if gen_ed < no_instance * 2 / 3:
            no_customer = random.randint(20, 50)
            no_trucks = random.randint(3, 6)
        else:
            no_customer = random.randint(70, 100)
            no_trucks = random.randint(6, 10)
        tight = random.uniform(0.82, 0.94)
        ins_name = "I%d-n%d-k%d" % (gen_ed + 1, no_customer, no_trucks)
        demand_variance = random.randint(0, 10)

        # Tạo instance:
        # Sinh tọa độ & demand cho tất cả điểm
        coordinates = []
        demands = []
        for i in range(no_customer):
            x, y, d = random.randint(0, 1000), random.randint(0, 1000), random.randint(1, 1 + demand_variance)
            coordinates.append((x, y))
            demands.append(d)
        # Demand depot auto = 0
        demands[0] = 0

        # sum demands = 100% tight => capacity?
        capacity = int(sum(demands) / (tight * no_trucks) + 1)

        # In ra theo đúng format CVRPLIB
        with open(data_path + ins_name + ".txt", 'w') as f:
            f.write("NAME: %s\n" % ins_name)
            f.write("COMMENT : (Fake et al, No of trucks: %d, Optimal value: )\n" % no_trucks)
            f.write("TYPE : CVRP\n")
            f.write("DIMENSION : %d\n" % no_customer)
            f.write("EDGE_WEIGHT_TYPE : EUC_2D\n")
            f.write("CAPACITY : %d\n" % capacity)
            f.write("NODE_COORD_SECTION\n")
            for i in range(no_customer):
                f.write("%d %d %d\n" %(i + 1, coordinates[i][0], coordinates[i][1]))
            f.write("DEMAND_SECTION\n")
            for i in range(no_customer):
                f.write("%d %d\n" %(i + 1, demands[i]))
            f.write("DEPOT_SECTION\n 1\n -1\n EOF ")
            gen_ed += 1


def delete_instance():
    print("Bấm F rồi Enter đê tiếp tục xóa dataset:")
    f = input()
    if f == "f":
        data_path = os.path.dirname(os.path.abspath(__file__)) + "\\Dataset\\Instance\\"
        for filename in os.listdir(data_path):
            if filename.startswith("I") and filename.endswith(".txt"):
                os.remove(os.path.join(data_path, filename))


# gen_instance(30000)
