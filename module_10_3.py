import threading
import time
import random
from random import randint


class Bank(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):

        for i in range(100):
            intake_ = randint(50, 500)
            self.balance += intake_
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            print(f"Пополнение: {intake_}. Баланс: {self.balance}.")
            time.sleep(0.001)

    def take(self):

        for i in range(100):
            pay_ = randint(50, 500)
            print(f"Запрос на {pay_}")
            if pay_ <= self.balance:
                self.balance -= pay_
                print(f"Снятие: {pay_}. Баланс: {self.balance}.")
            else:
                print("Запрос отклонен. Недостаточно средств")
                self.lock.acquire()

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')