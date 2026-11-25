"""Secure file vault with path resolution."""

import os

VAULT_ROOT = os.path.join(os.path.dirname(__file__), "vault")

_vault_files: dict[str, str] = {
    "reports/q1.pdf": "Q1 earnings summary",
    "reports/q2.pdf": "Q2 earnings summary",
}


def reset() -> None:
    os.makedirs(VAULT_ROOT, exist_ok=True)
    for rel_path, content in _vault_files.items():
        full = os.path.join(VAULT_ROOT, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)


def resolve_path(relative_path: str) -> str:
    return os.path.join(VAULT_ROOT, relative_path)


def read_file(relative_path: str) -> str | None:
    full_path = resolve_path(relative_path)
    if not os.path.isfile(full_path):
        return None
    with open(full_path, encoding="utf-8") as fh:
        return fh.read()
