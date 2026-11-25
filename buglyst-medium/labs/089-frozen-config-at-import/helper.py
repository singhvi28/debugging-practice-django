"""Application configuration loaded from environment variables."""

import os

FEATURE_BETA = os.getenv("FEATURE_BETA", "off")


def feature_beta_enabled() -> bool:
    return FEATURE_BETA == "on"
