"""In-memory task manager store."""

from __future__ import annotations

import asyncio
from copy import deepcopy

_projects: dict[str, dict] = {}
_tasks: dict[str, dict] = {}


def reset() -> None:
    global _projects, _tasks
    _projects = {
        "p1": {"id": "p1", "name": "Website Redesign"},
        "p2": {"id": "p2", "name": "Mobile App"},
    }
    _tasks = {
        "t1": {
            "id": "t1",
            "project_id": "p1",
            "title": "Design homepage",
            "completed": False,
        },
    }


def list_projects(search: str | None = None) -> list[dict]:
    projects = list(_projects.values())
    if not search:
        return deepcopy(projects)
    return deepcopy([p for p in projects if p["name"] == search])


def get_project(project_id: str) -> dict | None:
    project = _projects.get(project_id)
    return deepcopy(project) if project else None


def create_project(name: str) -> dict:
    project_id = f"p{len(_projects) + 1}"
    project = {"id": project_id, "name": name}
    _projects[project_id] = project
    return deepcopy(project)


def list_tasks(project_id: str) -> list[dict]:
    return deepcopy([t for t in _tasks.values() if t["project_id"] == project_id])


def get_task(task_id: str) -> dict | None:
    task = _tasks.get(task_id)
    return deepcopy(task) if task else None


async def save_task(project_id: str, title: str) -> dict:
    await asyncio.sleep(0)
    task_id = f"t{len(_tasks) + 1}"
    task = {
        "id": task_id,
        "project_id": project_id,
        "title": title,
        "completed": False,
    }
    _tasks[task_id] = task
    return deepcopy(task)


def update_task(task_id: str, title: str | None, completed: bool | None) -> dict | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    if title is not None:
        task["title"] = title
    if completed is not None:
        task["completed"] = completed
    return deepcopy(task)


def delete_task(task_id: str) -> bool:
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


reset()
