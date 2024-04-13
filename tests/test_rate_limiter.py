import pytest
from unittest.mock import Mock, patch
from src.rate_limiter import RateLimiter


# Helper function to advance time in the mock
def advance_time(start, advance_by):
    return Mock(side_effect=lambda: start + advance_by)


# Test to ensure requests are allowed under the limit
def test_rate_limiter_allows_requests_under_limit():
    limit = 5
    period = 60
    rate_limiter = RateLimiter(limit, period)

    with patch("time.time", return_value=100):
        for _ in range(limit):
            rate_limiter.check()  # This should allow all requests without sleeping

        assert rate_limiter.requests == limit


# Test to ensure the rate limiter waits for the correct amount of time
def test_rate_limiter_waits_correctly():
    limit = 1
    period = 2  # 2 seconds period for testing
    rate_limiter = RateLimiter(limit, period)

    with patch("time.time", return_value=100) as mock_time, patch(
        "time.sleep"
    ) as mock_sleep:
        rate_limiter.check()
        assert rate_limiter.requests == 1

        # Move time forward by less than the period and attempt to check again
        mock_time.side_effect = advance_time(mock_time.return_value, period - 0.5)
        rate_limiter.check()

        # Check that sleep was called with the correct number of seconds
        mock_sleep.assert_called_once_with(0.5)


# Test to ensure the limiter resets after the period has passed
def test_rate_limiter_resets_after_period():
    limit = 1
    period = 1  # 1 second period for testing
    rate_limiter = RateLimiter(limit, period)

    with patch("time.time", Mock(side_effect=[100, 100, 101])) as mock_time, patch(
        "time.sleep"
    ) as mock_sleep:
        # The first check sets the start time to 100
        rate_limiter.check()

        # The second check should simulate the period has passed
        mock_time.side_effect = advance_time(mock_time.side_effect[-1], period)
        rate_limiter.check()

        assert rate_limiter.requests == 1
        mock_sleep.assert_not_called()
