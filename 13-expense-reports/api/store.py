"""In-memory expense reports store."""

from __future__ import annotations

from copy import deepcopy

_reports: dict[str, dict] = {}


def reset() -> None:
    global _reports
    _reports = {
        "rep1": {
            "id": "rep1",
            "title": "Q2 Travel",
            "owner": "alice",
            "status": "draft",
            "lines": [],
        },
        "rep2": {
            "id": "rep2",
            "title": "Conference",
            "owner": "bob",
            "status": "submitted",
            "lines": [{"description": "Flight", "amount": 450.0}],
        },
    }


def list_reports() -> list[dict]:
    return deepcopy(list(_reports.values()))


def get_report(report_id: str) -> dict | None:
    report = _reports.get(report_id)
    return deepcopy(report) if report else None


def create_report(title: str, owner: str) -> dict:
    report_id = f"rep{len(_reports) + 1}"
    report = {
        "id": report_id,
        "title": title,
        "owner": owner,
        "status": "draft",
        "lines": [],
    }
    _reports[report_id] = report
    return deepcopy(report)


def submit_report(report_id: str) -> dict | None:
    report = _reports.get(report_id)
    if report is None:
        return None
    report["status"] = "submitted"
    return deepcopy(report)


def approve_report(report_id: str) -> dict | None:
    report = _reports.get(report_id)
    if report is None:
        return None
    updated = deepcopy(report)
    updated["status"] = "approved"
    return updated


def add_line_item(report_id: str, description: str, amount: float) -> dict | None:
    report = _reports.get(report_id)
    if report is None:
        return None
    report["lines"].append({"description": description, "amount": amount})
    return deepcopy(report)


reset()
