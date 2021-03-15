from fei.ppds import Semaphore, print, Thread
from time import sleep
from random import randint


class Shared:
    def __init__(self, n):
        self.n = n
        self.forks = [0] * self.n
        self.footman = Semaphore(n // 2)

        for i in range(self.n):
            self.forks[i] = Semaphore(1)

    def get_forks(self, i):
        self.footman.wait()
        print("thread %s called the footman" % (i))
        ''' right fork '''
        self.forks[i].wait()
        ''' left fork '''
        self.forks[(i + 1) % self.n].wait()

    def put_forks(self, i):
        ''' right fork '''
        self.forks[i].signal()
        ''' left fork '''
        self.forks[(i + 1) % self.n].signal()
        print("thread %s is finishing" % (i))
        self.footman.signal()


def think():
    sleep(0.5 + (randint(1, 5) / 10))


def eat():
    sleep(randint(1, 10) / 10)


def dining(SharedObject, thread):
    while True:
        think()
        SharedObject.get_forks(thread)
        eat()
        SharedObject.put_forks(thread)
        think()


num_philosophers = 5
shared_object = Shared(num_philosophers)

threads = list()

for i in range(num_philosophers):
    t = Thread(dining, shared_object, i)
    threads.append(t)

for t in threads:
    t.join()
