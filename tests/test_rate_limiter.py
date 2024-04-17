import pytest
import time
from unittest.mock import patch, Mock
from src.rate_limiter import RateLimiter


def test_initialization():
    """Test the RateLimiter initializes with correct values."""
    rl = RateLimiter(limit=10, period=60)
    assert rl.limit == 10
    assert rl.period == 60
    assert rl.requests == 0


def test_initialization_failure():
    """Test that initialization fails with incorrect values."""
    with pytest.raises(ValueError):
        RateLimiter(limit=-1, period=60)
    with pytest.raises(ValueError):
        RateLimiter(limit=10, period="a")


def test_request_limiting():
    """Test that RateLimiter correctly counts and limits requests."""
    rl = RateLimiter(limit=5, period=10)
    for i in range(5):
        rl.check()

    # Mock sleep to verify that it is called
    with patch("time.sleep", return_value=None) as mock_sleep:
        rl.check()
        mock_sleep.assert_called()


def test_period_expiration():
    """Test that RateLimiter resets after the period expires."""
    rl = RateLimiter(limit=2, period=2)  # Short period for test
    rl.check()
    rl.check()
    time.sleep(2.1)  # Sleep to ensure period expires
    try:
        rl.check()  # Should not raise an error if reset is working
    except Exception as e:
        pytest.fail(f"Period did not reset as expected: {e}")


# Test to ensure requests are allowed under the limit
def test_rate_limiter_allows_requests_under_limit():
    limit = 5
    period = 60
    rate_limiter = RateLimiter(limit, period)

    with patch("time.time", return_value=100):
        for _ in range(limit):
            rate_limiter.check()  # This should allow all requests without sleeping

        assert rate_limiter.requests == limit


# Test instantiation errors
@pytest.mark.parametrize(
    "limit,period", [(-1, 60), (5, -10), ("five", 60), (5, "sixty")]
)
def test_bad_instantiation(limit, period):
    with pytest.raises(ValueError):
        RateLimiter(limit, period)
