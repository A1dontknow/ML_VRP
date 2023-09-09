import os
import time

if __name__ == "__main__":
    solved = 0
    while 1:
        now = len(os.listdir("C:\\Users\Dell\PycharmProjects\pythonProject2\Dataset\Solution\ALNS"))
        if now > solved:
            solved = now
            print("Solved: %d / 60024" % now)
        time.sleep(1)