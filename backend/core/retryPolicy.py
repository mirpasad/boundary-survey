from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import httpx

# Configure retry policy
RETRY_POLICY = retry(
    stop=stop_after_attempt(3),  # Max 3 attempts
    wait=wait_exponential(multiplier=1, min=1, max=10),  # Exponential backoff
    retry=(
        retry_if_exception_type(httpx.ReadTimeout) |
        retry_if_exception_type(httpx.ConnectTimeout) |
        retry_if_exception_type(httpx.NetworkError) |
        retry_if_exception_type(httpx.HTTPStatusError)
    ),
    reraise=True
)