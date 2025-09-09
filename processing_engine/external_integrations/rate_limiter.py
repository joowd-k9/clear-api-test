"""Rate limiting utilities for external API clients."""

import time
import threading


class RateLimiter:
    """Simple token bucket rate limiter."""

    def __init__(self, rate: int, per: int):
        """
        Args:
            rate: number of requests allowed
            per: time window in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self):
        """Block until a request can be made."""
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_check
            self.last_check = now
            self.allowance += elapsed * (self.rate / self.per)
            self.allowance = min(self.allowance, self.rate)

            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                time.sleep(sleep_time)
                self.allowance = 0
            else:
                self.allowance -= 1.0
