import multiprocessing
import threading
import time

def read_info(name):
    all_data = []
    with open(name, "r") as file:
        all_data += file.readlines()


filenames = [f'./file {number}.txt' for number in range(1, 5)]

"""st_t_ = time.time()
for i in filenames:
    read_info(i)
fin_t_ = time.time()
print(fin_t_ - st_t_)"""

if __name__ == '__main__':

    st_t_ = time.time()
    with multiprocessing.Pool() as pool:
        pool.map(read_info, filenames)
    fin_t_ = time.time()
    print(fin_t_-st_t_)