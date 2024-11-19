import threading
import time
import random
from queue import Queue

class Table:

    def __init__(self, number, guest = None):
        self.number = number
        self.guest = guest

class Guest(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        time.sleep(random.randint(3, 10))

class Cafe(Table, Guest):

    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = []
        for i in tables:
            self.tables.append(i)

    def guest_arrival(self, *guests):
        for g in guests:
            gfl_1 = False
            gfl_2 = False
            for t in self.tables:
                if t.guest == None:
                    t.guest = g.name
                    Guest(t.guest).start()

                    print(f"{t.guest} сел(-а) за стол номер {t.number}")
                    gfl_1 = True

                    #print(threading.current_thread())
                    break
                else:
                    gfl_2 = True
            if not gfl_1 and gfl_2:
                self.queue.put(g)
                print(f"{g.name} в очереди")

    """def discuss_guest(self):

        while not self.queue.empty() or threading.current_thread().is_alive():
            if """




# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
print(threading.current_thread())