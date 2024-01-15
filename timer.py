from cmu_graphics import *
import time

# Citation: https://realpython.com/python-timer/#using-the-python-timer-class

class Timer:
    def __init__(self):
        self.startTime = None

    def start(self):
        self.startTime = time.perf_counter()

    def stop(self, target):
        elapsedTime = time.perf_counter() - self.startTime
        if target < elapsedTime:
            return True
        return False