from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.c = 0
        self.m = Mutex()
        self.b = Semaphore(0)

    def wait(self):
        self.m.lock()
        self.c += 1
        if (self.c == self.N):
            self.c = 0
            for i in range(self.N):
                self.b.signal()
        self.m.unlock()
        self.b.wait()


def rendezvous(thread_name):
    sleep(randint(1, 10) / 5)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(sb1, sb2, thread_name):
    while True:
        rendezvous(thread_name)
        sb1.wait()
        ko(thread_name)
        sb2.wait()


sb1 = SimpleBarrier(5)
sb2 = SimpleBarrier(5)

threads = list()

for i in range(5):
    t = Thread(barrier_example, sb1, sb2, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()
