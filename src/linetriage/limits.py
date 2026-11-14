"""Usage limits for the public website, so visitors can't drain the API credit.

Each visitor (IP address) gets MAX_PER_MINUTE triages a minute, and the whole
site gets MAX_PER_DAY a day. Both can be changed with environment variables.
Counts live in memory, so they reset when the server restarts.
"""

import os
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, per_minute: int, per_day: int):
        self.per_minute = per_minute
        self.per_day = per_day
        self.reset()

    def reset(self) -> None:
        self.recent: dict[str, deque[float]] = defaultdict(deque)
        self.day = time.strftime("%Y-%m-%d")
        self.today = 0

    def check(self, visitor: str, now: float | None = None) -> str | None:
        """Record one request. Returns a reason if it's over a limit, else None."""
        now = time.time() if now is None else now
        day = time.strftime("%Y-%m-%d", time.gmtime(now))
        if day != self.day:
            self.day, self.today = day, 0
        if self.today >= self.per_day:
            return "The live demo has reached today's limit. Please try again tomorrow, or run it locally."
        window = self.recent[visitor]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= self.per_minute:
            return "Too many requests. Please wait a minute and try again."
        window.append(now)
        self.today += 1
        return None


limiter = RateLimiter(
    per_minute=int(os.environ.get("LINETRIAGE_MAX_PER_MINUTE", "8")),
    per_day=int(os.environ.get("LINETRIAGE_MAX_PER_DAY", "300")),
)
