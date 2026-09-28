import time
import functools

# HTTP status codes that mean "try again later", not "your request is wrong"
TRANSIENT_CODES = {429, 500, 502, 503, 504}


def _is_transient(e: Exception) -> bool:
    code = getattr(e, "code", None)  # google.genai API errors carry an HTTP code
    if code is not None:
        return code in TRANSIENT_CODES
    return isinstance(e, (ConnectionError, TimeoutError))


def retry_with_backoff(max_attempts: int = 4, base_delay: float = 3.0):
    """
    Retry on transient failures only, with exponential backoff
    (3s, 6s, 12s by default). Non-transient errors are raised immediately.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not _is_transient(e) or attempt == max_attempts:
                        raise
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f"[{func.__name__}] attempt {attempt} failed ({e}); retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator