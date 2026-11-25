"""Environment flag parsing helpers."""

import os


def env_flag(name: str, default: str = "") -> bool:
    value = os.environ.get(name, default)
    return value.lower() != "false"


def maintenance_enabled() -> bool:
    return env_flag("MAINTENANCE_MODE")
