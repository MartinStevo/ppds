from fei.ppds import Semaphore, Thread, print, Mutex
from time import sleep
from random import randint


class Shared():
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.agent_sem = Semaphore(1)
        self.mutex = Mutex()

        self.numTobacco = 0
        self.numPaper = 0
        self.numMatch = 0

        self.semTobacco = Semaphore(0)
        self.semPaper = Semaphore(0)
        self.semMatch = Semaphore(0)


def make_cigarette():
    sleep(randint(0, 10) / 100)


def smoke():
    sleep(randint(0, 10) / 100)


def agent_1(shared_object):
    while True:
        sleep(randint(0, 10) / 100)
        # shared_object.agent_sem.wait()
        print("agent: paper, match")
        shared_object.paper.signal()
        shared_object.match.signal()


def agent_2(shared_object):
    while True:
        sleep(randint(0, 10) / 100)
        # shared_object.agent_sem.wait()
        print("agent: match, tobacco")
        shared_object.match.signal()
        shared_object.tobacco.signal()


def agent_3(shared_object):
    while True:
        sleep(randint(0, 10) / 100)
        # shared_object.agent_sem.wait()
        print("agent: tobacco, paper")
        shared_object.tobacco.signal()
        shared_object.paper.signal()


def smoker_1(shared_object):
    while True:
        sleep(randint(0, 10) / 100)

        shared_object.semMatch.wait()
        print("smoker with match: making cigarette")
        make_cigarette()

        # shared_object.agent_sem.signal()
        print("smoker with match: smoking")
        smoke()


def smoker_2(shared_object):
    while True:
        sleep(randint(0, 10) / 100)

        shared_object.semPaper.wait()
        print("smoker with paper: making cigarette")
        make_cigarette()

        # shared_object.agent_sem.signal()
        print("smoker with paper: smoking")
        smoke()


def smoker_3(shared_object):
    while True:
        sleep(randint(0, 10) / 100)

        shared_object.semTobacco.wait()
        print("smoker with tobacco: making cigarette")
        make_cigarette()

        # shared_object.agent_sem.signal()
        print("smoker with tobacco: smoking")
        smoke()


def dealer_1(shared_object):
    while True:
        sleep(randint(0, 10) / 100)

        shared_object.match.wait()

        shared_object.mutex.lock()
        print("dealer: match")
        if (shared_object.numPaper > 0):
            shared_object.numPaper -= 1
            shared_object.semTobacco.signal()

        elif (shared_object.numTobacco > 0):
            shared_object.numTobacco -= 1
            shared_object.semPaper.signal()

        else:
            shared_object.numMatch += 1
            print("match quantity: %d" % (shared_object.numMatch))
        shared_object.mutex.unlock()


def dealer_2(shared_object):
    while True:
        sleep(randint(0, 10) / 100)

        shared_object.paper.wait()

        shared_object.mutex.lock()
        print("dealer: paper")
        if (shared_object.numTobacco > 0):
            shared_object.numTobacco -= 1
            shared_object.semMatch.signal()

        elif (shared_object.numMatch > 0):
            shared_object.numMatch -= 1
            shared_object.semTobacco.signal()

        else:
            shared_object.numPaper += 1
            print("paper quantity: %d" % (shared_object.numPaper))
        shared_object.mutex.unlock()


def dealer_3(shared_object):
    while True:
        sleep(randint(0, 10) / 100)

        shared_object.tobacco.wait()

        shared_object.mutex.lock()
        print("dealer: tobacco")
        if (shared_object.numMatch > 0):
            shared_object.numMatch -= 1
            shared_object.semPaper.signal()

        elif (shared_object.numPaper > 0):
            shared_object.numPaper -= 1
            shared_object.semMatch.signal()

        else:
            shared_object.numTobacco += 1
            print("tobacco quantity: %d" % (shared_object.numTobacco))
        shared_object.mutex.unlock()


shared = Shared()

smokers = []
smokers.append(Thread(smoker_1, shared))
smokers.append(Thread(smoker_2, shared))
smokers.append(Thread(smoker_3, shared))

dealers = []
dealers.append(Thread(dealer_1, shared))
dealers.append(Thread(dealer_2, shared))
dealers.append(Thread(dealer_3, shared))

agents = []
agents.append(Thread(agent_1, shared))
agents.append(Thread(agent_2, shared))
agents.append(Thread(agent_3, shared))

for t in agents + smokers + dealers:
    t.join()
