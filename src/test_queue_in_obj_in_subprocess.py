from multiprocessing import Process, Queue
import time

"""
Test to make sure it is possible to communicate between 2 subprocesses using a queue passed via an object for one and the raw queue for the other.
"""

class Obj:
    def __init__(self, q):
        self.q = q

def test_1(o):
    while True:
        o.q.put('Woaw')
        time.sleep(1)

def test_2(q):
    while True:
        while not q.empty():
            print(q.get())
        time.sleep(0.5)

q = Queue()
o = Obj(q)
p1 = Process(target=test_1, args=(o,))
p1.start()
p2 = Process(target=test_2, args=(q,))
p2.start()

time.sleep(10)
p1.terminate()
p2.terminate()
print('Over')
