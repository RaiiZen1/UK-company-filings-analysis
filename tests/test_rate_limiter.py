import pytest
from unittest.mock import Mock, patch
from src.rate_limiter import RateLimiter


# Test to ensure requests are allowed under the limit
def test_rate_limiter_allows_requests_under_limit():
    limit = 5
    period = 60
    rate_limiter = RateLimiter(limit, period)

    for _ in range(limit):
        rate_limiter.check()  # This should allow all requests without sleeping

    assert rate_limiter.requests == limit


# Test to ensure the rate limiter waits for the correct amount of time
def test_rate_limiter_waits_correctly():
    limit = 1
    period = 2  # 2 seconds period for testing
    rate_limiter = RateLimiter(limit, period)

    with patch("time.time", return_value=100), patch("time.sleep") as mock_sleep:
        rate_limiter.check()
        assert rate_limiter.requests == 1

        # Move time forward by less than the period and attempt to check again
        rate_limiter.start_time = 98  # 2 seconds before current mocked time
        rate_limiter.check()

        # Check that sleep was called with the correct number of seconds
        mock_sleep.assert_called_with(period)


# Test to ensure the limiter resets after the period has passed
def test_rate_limiter_resets_after_period():
    limit = 1
    period = 1  # 1 second period for testing
    rate_limiter = RateLimiter(limit, period)

    with patch("time.time", Mock(side_effect=[100, 100, 101])):
        # The first check sets the start time to 100
        rate_limiter.check()

        # The second check is still within the period, and should hit the rate limit
        with pytest.raises(RuntimeError):
            rate_limiter.check()

        # After the period has passed, the limiter should reset and allow the next request
        rate_limiter.check()
        assert rate_limiter.requests == 1
