from fei.ppds import Mutex, print, Semaphore, Thread, Event
from time import sleep
from random import randint


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
        sleep(0.5)
        turnstile.wait()
        monitor_num = ls_monitor.lock(access_data)
        turnstile.signal()
        print('monitor id: %d number of monitors reading: %d' %
              (monitor_id, monitor_num))
        ls_monitor.unlock(access_data)


def sensor(sensor_id, access_data, turnstile, ls_sensor, valid_data):
    while True:
        sleep(0.5)
        turnstile.wait()
        turnstile.signal()
        sensor_num = ls_sensor.lock(access_data)
        writing_time = 0.01 + (randint(0, 5) / 1000)
        print("sensor id: %d number of sensors writing: %d writing time %.3f" %
              (sensor_id, sensor_num, writing_time))
        sleep(writing_time)
        valid_data.signal()
        ls_sensor.unlock(access_data)


access_data = Semaphore(1)
turnstile = Semaphore(1)
ls_monitor = Lightswitch()
ls_sensor = Lightswitch()
valid_data = Event()

for i in range(2):
    t = Thread(monitor, i, access_data, turnstile, ls_monitor, valid_data)
    pass
for i in range(11):
    t = Thread(sensor, i, access_data, turnstile, ls_sensor, valid_data)
