"""Circuit breaker for downstream calls."""

FAILURE_THRESHOLD = 3
PROBE_LIMIT = 1

_state = "closed"
_failure_count = 0
_half_open_probes = 0


def reset_circuit() -> None:
    global _state, _failure_count, _half_open_probes
    _state = "closed"
    _failure_count = 0
    _half_open_probes = 0


def circuit_state() -> str:
    return _state


def half_open_probe_count() -> int:
    return _half_open_probes


def record_failure() -> None:
    global _state, _failure_count
    _failure_count += 1
    if _failure_count >= FAILURE_THRESHOLD:
        _state = "open"


def trip_to_half_open() -> None:
    global _state, _half_open_probes
    _state = "half_open"
    _half_open_probes = 0


def record_success() -> None:
    global _state, _failure_count, _half_open_probes
    _state = "closed"
    _failure_count = 0
    _half_open_probes = 0


def allow_request() -> bool:
    global _half_open_probes
    if _state == "open":
        return False
    if _state == "half_open":
        _half_open_probes += 1
        return True
    return True
