from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.c = 0
        self.m = Mutex()
        self.t1 = Semaphore(0)
        self.t2 = Semaphore(1)

    def wait(self):
        self.m.lock()
        self.c += 1
        if (self.c == self.N):
            self.t2.wait()
            self.t1.signal()
        self.m.unlock()
        self.t1.wait()
        self.t1.signal()

        self.m.lock()
        self.c -= 1
        if (self.c == 0):
            self.t1.wait()
            self.t2.signal()
        self.m.unlock()
        self.t2.wait()
        self.t2.signal()


def rendezvous(thread_name):
    sleep(randint(1, 10) / 5)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_example(sb, thread_name):
    while True:
        rendezvous(thread_name)
        sb.wait()
        ko(thread_name)
        sb.wait()


sb = SimpleBarrier(5)

threads = list()

for i in range(5):
    t = Thread(barrier_example, sb, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()
