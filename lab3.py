import time
import numpy as np
import math


class TimeStats:
    def __init__(self):
        self.times = []

    def add(self, t):
        self.times.append(t)

    @property
    def count(self):
        return len(self.times)

    @property
    def min(self):
        return min(self.times) if self.times else None

    @property
    def max(self):
        return max(self.times) if self.times else None

    @property
    def avg(self):
        return sum(self.times) / len(self.times) if self.times else None

    @property
    def std(self):
        if len(self.times) < 2:
            return None
        mean = self.avg
        return math.sqrt(sum((t - mean) ** 2 for t in self.times) / (len(self.times) - 1))

    def __str__(self):
        return (
            f"Wywołania: {self.count}\n"
            f"Min   : {self.min:.6f} s\n"
            f"Max   : {self.max:.6f} s\n"
            f"Srednia: {self.avg:.6f} s\n"
            f"Std   : {self.std:.6f} s"
        )

def measureTime(statsObj):
    def decorator(func):
        def wrapper():
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            statsObj.add(end - start)
        return wrapper
    return decorator



stats = TimeStats()

@measureTime(stats)
def timedFunction():
    A = np.random.rand(1000, 1000)
    B = np.random.rand(1000, 1000)
    return A @ B

for i in range(20):
    timedFunction()

print(stats)