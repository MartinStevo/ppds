import numpy as np
import fei.ppds as ppds


class Shared():
    def __init__(self, n):
        self.counter = 0
        self.end = n
        self.elms = np.zeros(self.end, dtype = int)
        pass


def func(sharedObject, mutex):
    while True:
        mutex.lock()
        if (sharedObject.counter >= sharedObject.end):
            mutex.unlock()
            break

        sharedObject.elms[sharedObject.counter] += 1
        sharedObject.counter += 1
        mutex.unlock()


for x in range(10):
    sharedObject = Shared(1000000)
    mutex = ppds.Mutex()

    thread1 = ppds.Thread(func, sharedObject, mutex)
    thread2 = ppds.Thread(func, sharedObject, mutex)
    thread1.join()
    thread2.join()

    hist = (np.histogram(sharedObject.elms, bins = [0,1,2,3]))
    print(hist)
    
