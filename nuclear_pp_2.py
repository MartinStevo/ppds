from fei.ppds import Mutex, print, Semaphore, Thread, Event
from time import sleep
from random import randint


class Barrier:
    def __init__(self, n):
        self.n = n
        self.c = 0
        self.m = Mutex()
        self.b = Event()

    def wait(self):
        self.m.lock()
        self.c += 1
        if (self.c == self.n):
            self.b.signal()
        self.m.unlock()
        self.b.wait()


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return self.counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def monitor(monitor_id, access_data, turnstile, ls_monitor, valid_data):
    valid_data.wait()
    while True:
        turnstile.wait()
        monitor_num = ls_monitor.lock(access_data)
        turnstile.signal()
        print('monitor id: %d number of monitors reading: %d' %
              (monitor_id, monitor_num))
        sleep(randint(50, 60) / 1000)
        ls_monitor.unlock(access_data)


def sensor(sensor_id, access_data, barrier, turnstile, ls_sensor, valid_data):
    while True:
        turnstile.wait()
        sensor_num = ls_sensor.lock(access_data)
        turnstile.signal()
        if (sensor_id == 0):
            writing_time = (randint(20, 25) / 1000)
        else:
            writing_time = (randint(10, 20) / 1000)
        print("sensor id: %d number of sensors writing: %d writing time %.3f" %
              (sensor_id, sensor_num, writing_time))
        sleep(writing_time)
        barrier.wait()
        valid_data.set()
        ls_sensor.unlock(access_data)


num_sensors = 3
access_data = Semaphore(1)
barrier = Barrier(num_sensors)
turnstile = Semaphore(1)
ls_monitor = Lightswitch()
ls_sensor = Lightswitch()
valid_data = Event()

for i in range(8):
    t = Thread(monitor, i, access_data, turnstile, ls_monitor, valid_data)
for i in range(3):
    t = Thread(sensor, i, access_data, barrier, turnstile, ls_sensor,
               valid_data)
