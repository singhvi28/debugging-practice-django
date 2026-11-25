"""Test spy for outbound calls."""

_call_log: list[str] = []
_call_count = 0


def reset_spy() -> None:
    _call_log.clear()


def record_call(name: str) -> None:
    global _call_count
    _call_count += 1
    _call_log.append(name)


def call_count() -> int:
    return _call_count


def call_log() -> list[str]:
    return list(_call_log)
