from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, Event
from fei.ppds import print


class FibonacciSeq:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.array = [0, 1]
        self.mutex = Mutex()
        self.sem_array = [0] * self.n
        self.event_array = [0] * self.n
        for i in range(self.n):
            self.sem_array[i] = Semaphore(0)
        for i in range(self.n):
            self.event_array[i] = Event()

    def do_count(self, thread_id):
        sleep(randint(1, 10) / 10)
        self.sem_array[int(thread_id)].signal()
        # self.event_array[int(thread_id)].signal()
        length = len(self.array)
        self.array.append(self.array[length - 1] + self.array[length - 2])
        print('Thread:\t%s\tFibonacci:\t%d' % (thread_id, self.array[length]))
        self.sem_array[int(thread_id)].wait()
        # self.event_array[int(thread_id)].clear()


def do_fibonacci_sequence(fs, thread_id):
    # while:
    #     fs.do_count(thread_id)
    fs.do_count(thread_id)


n = 100

fs = FibonacciSeq(n)

threads = list()

for i in range(n):
    t = Thread(do_fibonacci_sequence, fs, '%d' % i)
    threads.append(t)

for t in threads:
    t.join()

print("\nTerminal array:\n")
print(fs.array)
