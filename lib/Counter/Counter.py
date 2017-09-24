from time import time


class Counter:

    def __init__(self, start, end, step=1, ttl=86400):
        self.start = 0
        self.one_step = step
        self.ttl = ttl
        self.current = start
        self.end = end
        self.start_time = time()

    def reset(self):
        self.set_current(self.start)
        self.set_start_time(time())

    def get_current(self):
        return self.current

    def set_current(self, val):
        self.current = val

    def get_start_time(self):
        return self.start_time

    def set_start_time(self, val):
        self.start_time = val

    def is_can(self):
        ttl_reset = (self.get_start_time() + self.ttl) < time()
        if ttl_reset:
            self.reset()

        return self.end > self.get_current()

    def step(self):
        self.set_current(self.get_current() + self.one_step)