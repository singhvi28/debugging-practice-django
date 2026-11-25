"""Environment configuration loader."""

import os
from pathlib import Path

_CONFIG: dict[str, str] = {}


def _parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_config() -> dict[str, str]:
    global _CONFIG
    base = Path(__file__).parent
    env_name = os.environ.get("ENVIRONMENT", "dev")
    env_file = base / ".env.dev"
    file_values = _parse_env_file(env_file)
    _CONFIG = {**file_values, **{k: v for k, v in os.environ.items() if k in file_values}}
    if "ENVIRONMENT" in os.environ:
        _CONFIG["ENVIRONMENT"] = os.environ["ENVIRONMENT"]
    elif env_name:
        _CONFIG["ENVIRONMENT"] = env_name
    return dict(_CONFIG)


def get_config() -> dict[str, str]:
    if not _CONFIG:
        load_config()
    return dict(_CONFIG)


def reset() -> None:
    global _CONFIG
    _CONFIG = {}
