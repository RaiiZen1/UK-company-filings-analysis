import time


class RateLimiter:
    def __init__(self, limit, period):
        self.requests = 0
        self.limit = limit
        self.period = period
        self.start_time = time.time()

    def check(self):
        if self.requests >= self.limit:
            elapsed_time = time.time() - self.start_time
            if elapsed_time < self.period:
                time.sleep(self.period - elapsed_time)
            self.requests = 0
            self.start_time = time.time()
        self.requests += 1
