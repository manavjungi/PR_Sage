import time
import functools


def retry_with_backoff(max_attempts: int = 3, base_delay: float = 2.0):
    """
    Decorator: retries a function on failure, with exponential backoff.
    e.g. delays of 2s, 4s, 8s between attempts (base_delay=2.0).
    Re-raises the last exception if all attempts fail.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    is_last_attempt = attempt == max_attempts
                    if is_last_attempt:
                        break
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f"[{func.__name__}] attempt {attempt} failed ({e}); retrying in {delay}s...")
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator