"""Latency percentile aggregation across services."""

_service_samples: dict[str, list[float]] = {}


def reset() -> None:
    _service_samples.clear()
    _service_samples["checkout"] = [10.0, 12.0, 14.0, 16.0, 200.0]
    _service_samples["search"] = [5.0, 6.0, 7.0, 8.0, 180.0]


def get_service_samples() -> dict[str, list[float]]:
    return {name: list(samples) for name, samples in _service_samples.items()}


def _percentile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    index = int(round((pct / 100) * (len(ordered) - 1)))
    return ordered[index]


def compute_p95(samples_by_service: dict[str, list[float]]) -> float:
    service_averages = [
        sum(samples) / len(samples) for samples in samples_by_service.values()
    ]
    return round(sum(service_averages) / len(service_averages), 2)
