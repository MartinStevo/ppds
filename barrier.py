from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
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
            self.b.signal()
        self.m.unlock()
        self.b.wait()
        self.b.signal()


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


n = 5
sb = SimpleBarrier(n)

threads = list()
for i in range(n):
    t = Thread(barrier_example, sb, i)
    threads.append(t)

for i in threads:
    t.join()
