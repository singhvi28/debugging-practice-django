"""Shared retry budget across concurrent callers."""

BUDGET_SIZE = 5


class BudgetExhausted(Exception):
    pass


class TransientError(Exception):
    pass


_remaining: int = BUDGET_SIZE


def reset_budget() -> None:
    global _remaining
    _remaining = BUDGET_SIZE


def budget_remaining() -> int:
    return _remaining


def consume_slot() -> None:
    global _remaining
    if _remaining <= 0:
        raise BudgetExhausted("retry budget exhausted")
    _remaining -= 1


def refund_slot() -> None:
    global _remaining
    if _remaining < BUDGET_SIZE:
        _remaining += 1


def run_with_budget(operation):
    """Run an operation, consuming one budget slot per attempt."""
    consume_slot()
    try:
        return operation()
    except TransientError:
        raise
