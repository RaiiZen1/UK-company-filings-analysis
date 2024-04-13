import pytest
from unittest.mock import patch, Mock
from src.rate_limiter import RateLimiter


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
