from fei.ppds import Mutex, Semaphore, Event, Thread, print
from time import sleep
from random import randint, choice


class Barrier():
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.barrier1 = Event()
        self.barrier2 = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if (self.counter == self.n):
            self.barrier2.clear()
            self.barrier1.set()
        self.mutex.unlock()
        self.barrier1.wait()

        self.mutex.lock()
        self.counter -= 1
        if (self.counter == 0):
            self.barrier1.clear()
            self.barrier2.set()
        self.mutex.unlock()
        self.barrier2.wait()


class Shared():
    def __init__(self):
        self.mutex = Semaphore(1)
        self.oxygen = 0
        self.hydrogen = 0
        self.oxygenQueue = Semaphore(0)
        self.hydrogenQueue = Semaphore(0)
        self.barrier = Barrier(3)


def bond(atom):
    print("%s" % (atom))
    sleep(randint(1, 10) / 100)


def oxygen(shared_object):
    shared_object.mutex.wait()
    shared_object.oxygen += 1
    print("atoms of oxygen: %d" % (shared_object.oxygen))
    if shared_object.hydrogen < 2:
        shared_object.mutex.signal()
    else:
        shared_object.oxygen -= 1
        shared_object.hydrogen -= 2
        shared_object.oxygenQueue.signal()
        shared_object.hydrogenQueue.signal(2)

    shared_object.oxygenQueue.wait()
    bond("O")

    shared_object.barrier.wait()
    print("molecule was formed\n")
    shared_object.mutex.signal()


def hydrogen(shared_object):
    shared_object.mutex.wait()
    shared_object.hydrogen += 1
    print("atoms of hydrogen: %d" % (shared_object.hydrogen))
    if shared_object.hydrogen < 2 or shared_object.oxygen < 1:
        shared_object.mutex.signal()
    else:
        shared_object.oxygen -= 1
        shared_object.hydrogen -= 2
        shared_object.oxygenQueue.signal()
        shared_object.hydrogenQueue.signal(2)

    shared_object.hydrogenQueue.wait()
    bond("H")

    shared_object.barrier.wait()


shared_object = Shared()
ch = [oxygen, hydrogen]

while True:
    Thread(choice(ch), shared_object)
    sleep(randint(1, 10) / 10)
