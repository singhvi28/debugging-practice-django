"""HTTP client for upstream calls."""

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from upstream import fetch_upstream

_executor = ThreadPoolExecutor(max_workers=1)


REQUEST_TIMEOUT_SECONDS = 0.1


def call_upstream() -> dict:
    future = _executor.submit(fetch_upstream)
    return future.result()
