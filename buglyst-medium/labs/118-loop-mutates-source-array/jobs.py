"""Background job runner."""

_processed: list[str] = []


def reset() -> None:
    _processed.clear()


def processed_jobs() -> list[str]:
    return list(_processed)


def process_jobs(jobs: list[dict]) -> list[str]:
    """Run pending jobs in order, skipping entries marked with skip=True."""
    completed: list[str] = []
    for job in jobs:
        if job.get("skip"):
            jobs.remove(job)
            continue
        job_id = job["id"]
        _processed.append(job_id)
        completed.append(job_id)
    return completed
