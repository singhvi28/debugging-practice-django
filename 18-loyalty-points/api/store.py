import threading
import time
from copy import deepcopy

_lock = threading.Lock()

_accounts = {
    "acct_1": {"id": "acct_1", "owner": "Alice", "balance": 500},
    "acct_2": {"id": "acct_2", "owner": "Bob", "balance": 120},
}

_ledger: dict[str, list[dict]] = {
    "acct_1": [],
    "acct_2": [],
}


def reset() -> None:
    global _accounts, _ledger
    _accounts = {
        "acct_1": {"id": "acct_1", "owner": "Alice", "balance": 500},
        "acct_2": {"id": "acct_2", "owner": "Bob", "balance": 120},
    }
    _ledger = {
        "acct_1": [],
        "acct_2": [],
    }


def list_accounts() -> list[dict]:
    return deepcopy(list(_accounts.values()))


def get_account(account_id: str) -> dict | None:
    account = _accounts.get(account_id)
    return deepcopy(account) if account else None


def get_balance(account_id: str) -> int | None:
    account = _accounts.get(account_id)
    if account is None:
        return None
    return account["balance"]


def earn_points(account_id: str, amount: int, reason: str) -> dict | None:
    account = _accounts.get(account_id)
    if account is None:
        return None
    account["balance"] += amount
    entry = {
        "type": "earn",
        "amount": amount,
        "reason": reason,
        "balance_after": account["balance"],
    }
    _ledger.setdefault(account_id, []).append(entry)
    return deepcopy(account)


def redeem_points(account_id: str, amount: int, reason: str) -> dict | None:
    account = _accounts.get(account_id)
    if account is None:
        return None
    with _lock:
        if account["balance"] < amount:
            return None
        time.sleep(0.05)
        entry = {
            "type": "redeem",
            "amount": amount,
            "reason": reason,
            "balance_after": account["balance"] - amount,
        }
        _ledger.setdefault(account_id, []).append(entry)
    return deepcopy(account)


def get_ledger(account_id: str) -> list[dict] | None:
    if account_id not in _accounts:
        return None
    return deepcopy(_ledger.get(account_id, []))


reset()
