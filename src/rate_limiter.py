import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimiter:
    """
    A rate limiter that limits the number of requests that can be made in a time period.

    Attributes:
        limit (int): The maximum number of requests that can be made in the given period.
        period (float): The time period in seconds during which requests are limited.
        requests (int): The current number of requests made in the period.
        start_time (float): The start time of the period.
    """

    def __init__(self, limit, period):
        """
        Initializes the rate limiter with a specified limit and time period.

        Args:
            limit (int): The maximum number of requests per time period.
            period (float): The time period in seconds.
        """
        if not isinstance(limit, int) or not isinstance(period, (int, float)):
            logger.error("Limit must be an integer and period must be a number.")
            raise ValueError("Limit must be an integer and period must be a number.")

        if limit <= 0 or period <= 0:
            logger.error("Limit and period must be greater than 0.")
            raise ValueError("Limit and period must be greater than 0.")

        self.requests = 0
        self.limit = limit
        self.period = period
        self.start_time = time.time()

    def check(self):
        """
        Check whether a new request can be made. If the limit has been reached within the period,
        sleep until the end of the period before allowing new requests.
        """
        if self.requests >= self.limit:
            elapsed_time = time.time() - self.start_time
            if elapsed_time < self.period:
                sleep_time = self.period - elapsed_time
                logger.info(
                    f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds."
                )
                time.sleep(sleep_time)
            self._reset_period()

        self.requests += 1
        logger.debug(
            f"Request allowed. {self.limit - self.requests} requests left in this period."
        )

    def _reset_period(self):
        """
        Reset the request count and start time at the end of a period.
        """
        self.requests = 0
        self.start_time = time.time()
