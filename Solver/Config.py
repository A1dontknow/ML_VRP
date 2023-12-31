import os

"""
    Cac tham so se duoc mo ta nhu sau:

        * Nhung tham so nen giu co dinh:
        - D: Deterministic level cho Shaw Destroy. Khong co khac biet nhieu neu thay doi
        - DESTROY_RATIO: Muc pha huy nghiem trong destroy operator (tru MassiveDestroy).
        Muc Destroy nen de la 10%

        * Nhung tham so co the tinh chinh:
        - ITERATION: So vong lap thuc hien thuat toan. Khi cho chay du lau, thuat toan se
        co the tim duoc nhung nghiem tot hon, nhung khong co nghia la cang lau cang tot.
        Chay thuat toan song song voi so lan lap nao do co the la mot y tuong tot
        - SEGMENT: So phan doan (anh huong den viec update trong so cho cac operator va tan suat
        su dung Local Search)
        - PHI_1: Diem thuong cho operator neu tim duoc nghiem tot nhat
        - PHI_2: Diem thuong cho operator neu tim duoc nghiem tot hon nghiem hien tai
        - PHI_3: Diem thuong neu nghiem tim duoc khong co su cai tien nao
        - N: Reaction factor - He so phan ung cua Adaptive Mechanism
        - V: Normalization factor - He so chuan hoa cua Adaptive Mechanism
        - DEVIATION: Chap nhan nghiem (ke ca nghiem xau hon) neu khong te hon mot nguong
        so voi nghiem tot nhat
        - BIG_DEVIATION: Chap nhan nghiem (ke ca nghiem xau hon) neu khong te hon mot nguong
        so voi nghiem tot nhat sau khi trai qua rat nhieu lan lap ma khong co su cai tien ve
        nghiem
        
        - EARLY STOP: Dung thuat toan khi dat den gap nhat dinh (gap do phai biet truoc)
        - OPTIMAL: Gia tri toi uu biet truoc
        - MIN_GAP / MAX_GAP: Specify do chenh lech so voi OPTIMAL de dung thuat toan som
        - alpha: Regularization. Only apply for non-early stop

"""
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
D = 5
ITERATION = 3000000
DESTROY_RATIO = 0.1
SEGMENT = 30000
PHI_1 = 10
PHI_2 = 6
PHI_3 = 1
N = 1
V = 1
DEVIATION = 20
BIG_DEVIATION = 100

PRINT_LOG = 1
EARLY_STOP = 0
OPTIMAL = 0
MIN_GAP = 0
MAX_GAP = 0
alpha = 0.1