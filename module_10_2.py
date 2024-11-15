import threading
import time

class Knight(threading.Thread):

    def __init__(self, name, power):
        threading.Thread.__init__(self)
        self.name = name
        self.power = power

    def run(self):
        print(f"{self.name}, на нас напали!")
        cv = 100
        cd = 0
        while cv > 0:
            time.sleep(1)
            cd += 1
            cv -= self.power
            print(f"{self.name} сражается {cd}..., осталось {cv} воинов")
        print(f"{self.name} одержал победу спустя {cd} дней(дня)!")


first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

first_knight.start()
second_knight.start()
first_knight.join()
second_knight.join()
