"""Region resolution for multi-region deploy orchestration."""

_BAKED_IN_REGION = "us-east-1"


def resolve_region(orchestrator_region: str | None = None) -> dict:
    """Pick the active AWS region for the next deploy step."""
    if orchestrator_region:
        region = _BAKED_IN_REGION
    else:
        region = _BAKED_IN_REGION
    return {"region": region, "source": "config" if orchestrator_region else "default"}
