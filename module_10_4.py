import threading
import time
import random
from queue import Queue

# создаём класс Table для столов
class Table:

    # Определяем метод init класса Table
    def __init__(self, number, guest = None):
        # в методе init создаем принимаемые классом атрибуты
        # первый атрибут number является целым числом
        self.number = number
        # второй атриьут это объек класса Guest
        self.guest = guest

# создаем класс Guest наследуемый от threading.Thread
class Guest(threading.Thread):

    # при создании объекта класса Guest необходимо вводить аргумент name
    def __init__(self, name):
        # переопределяем метод init родительского класса
        threading.Thread.__init__(self)
        # создаем атрибут name для класса Guest
        self.name = name

    # переопределяем метод run для класса Thread в классе Guest
    def run(self):
        time.sleep(random.randint(3, 10))

# создаем класс Cafe
class Cafe:

    # определяем метод init для класса Cafe
    # здесь указываем, что для создания класса необходимо вводить аргумент: объект класса Table
    def __init__(self, *tables):
        # создаем атрибут queue, который является объектом класса Queue
        self.queue = Queue()
        # здесь создаем атрибут tables, который принимает коллекцию объектов класса Table
        self.tables = list(tables)
        # создаём атрибут lock для разграничения работы потоков
        self.lock = threading.Lock()

    # определяем метод прибытия гостей
    def guest_arrival(self, *guests):
        # так как метод предусматривает в качестве аргумента коллекцию объектов класса Guest
        # создаем цикл, который будет перебирать каждый объект Guest
        for g in guests:
            # здесь мы создали флаг, чтобы в дальнейшем определить,
            # какие объекты класса Guest попадут в очередь
            seated = False

            # чтобы упростить код используем конструкцию with для работы с Lock
            with self.lock:
                # организуем цикл, где перебираем объекты класса Table
                for t in self.tables:
                    # здесь мы задаем условие, при котором мы сажаем гостей за столы
                    # (запускаем потоки Guest если гость сидит за столом)
                    # и если гостя за столом нет, сажаем гостя за стол, а именно
                    if t.guest is None:
                        # атрибуту класса Table присваеваем объект класса Guest
                        t.guest = g
                        # когда посадили гостя за стол, запускаем поток гостя
                        g.start()
                        # выводим f-строку
                        print(f"{t.guest.name} сел(-а) за стол номер {t.number}")
                        # здесь задаем флагу True. Это проверка сидит ли гость за столом
                        seated = True
                        # когда мы посадили гостя за стол нам нет нужды перебирать оставшиеся столы
                        # поэтому прерываем работу цикла
                        break

                # здесь мы проверяем, если после работы цикла никого за стол не посадили
                # то гостя следует отправить в очередь
                if not seated:
                    self.queue.put(g)
                    print(f"{g.name} в очереди")

    # определяем метод обслуживания гостей
    def discuss_guests(self):

        # здесь согласно условию задачи необходимо задать условие для работы цикла while
        # если очередь не пуста или за столом еще ктото сидит
        # чтобы определить сидит ли кто за столом испоьзуем метод any для сгенерированного списка
        # где в список попадают все аргументы, где гость сидит за столом
        while not self.queue.empty() or any(t.guest is not None for t in self.tables):

            with self.lock:

                # в цикле проверяем, какие гости покушали (поток Guest прекратил работу)
                # для этого перебираем все столы
                for t in self.tables:

                    # создаем условие для проверки
                    # если стол занят и поток прекратил свою работу
                    if t.guest is not None and not t.guest.is_alive():
                        # выводим f-строку
                        print(f'{t.guest.name} покушал(-а) и ушёл(ушла)')
                        # опустошаем атрибут гостя класса Table
                        t.guest = None
                        # выводим f-строку
                        print(f'Стол номер {t.number} свободен')

                        # в этом же условии, когда стол освободился проверяем, пустая ли очередь
                        if not self.queue.empty():
                            # и если очередь не пустая, то сразу же сажаем за освободившийся стол
                            # первого гостя в очереди и убираем его из очереди
                            t.guest = self.queue.get()
                            # как посадили гостя, запускаем его поток
                            t.guest.start()
                            # выводим f-строку
                            print(f'{t.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {t.number}')


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
# Обслуживание гостей
cafe.discuss_guests()