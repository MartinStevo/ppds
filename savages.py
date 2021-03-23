from fei.ppds import Semaphore, Mutex, Thread, print, Event
from random import randint
from time import sleep


class SimpleBarrier:

    def __init__(self, n):
        self.n = n
        self.mutex = Mutex()
        self.counter = 0
        self.sem = Semaphore(0)

    def wait(self, sem, thread_id):
        rendezvous(thread_id)
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.sem.signal(self.n)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.counter = 0
        self.mutex = Mutex()
        self.servings = 0
        self.barrier_savages = SimpleBarrier(self.n)
        self.barrier_cooks = SimpleBarrier(self.m)
        self.meeting_savages = Semaphore(0)
        self.meeting_cooks = Semaphore(0)
        self.emptyPot = Event()
        self.fullPot = Semaphore(0)


def rendezvous(thread_id):
    sleep(randint(1, 10) / 100)
    print("rendezvous: %s" % (thread_id))


def get_serving_from_pot(thread_id):
    sleep(randint(1, 10) / 100)
    print("getting serving from pot: %s" % (thread_id))


def put_servings_in_pot(thread_id):
    sleep(randint(1, 10) / 100)
    print("putting servings in pot by: %s" % (thread_id))


def eat(thread_id):
    sleep(randint(1, 10) / 10)
    print("eating: %s" % (thread_id))


def cook(num_cooks, thread_id):
    sleep(randint(1, 10) / (10 * num_cooks))
    print("cooking: %s" % (thread_id))


def savage_thread(shared_object, thread_id):
    while True:
        shared_object.barrier_savages.wait(
            shared_object.meeting_savages, thread_id)
        shared_object.mutex.lock()
        if shared_object.servings == 0:
            shared_object.emptyPot.set()
            shared_object.fullPot.wait()

        shared_object.servings -= 1
        get_serving_from_pot(thread_id)
        shared_object.mutex.unlock()
        eat(thread_id)
        ''' rest after eating
        '''
        sleep(randint(1, 3))


def cook_thread(shared_object, thread_id):
    while True:
        shared_object.emptyPot.wait()
        shared_object.barrier_cooks.wait(
            shared_object.meeting_cooks, thread_id)
        cook(shared_object.m, thread_id)
        shared_object.counter += 1
        shared_object.emptyPot.clear()
        if (shared_object.counter == shared_object.m):
            shared_object.counter = 0
            put_servings_in_pot(thread_id)
            shared_object.servings = shared_object.n
            print("%d new servings in pot" % (shared_object.servings))
            shared_object.fullPot.signal()


num_savages = 10
num_cooks = 2

shared_object = Shared(num_savages, num_cooks)

savages = list()
cooks = list()

for i in range(num_savages):
    t = Thread(savage_thread, shared_object, "savage %d" % i)
    savages.append(t)

for i in range(num_cooks):
    t = Thread(cook_thread, shared_object, "cook %d" % i)
    cooks.append(t)

for s in savages + cooks:
    s.join()
