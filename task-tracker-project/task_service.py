from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from task_store import get_next_task_id, load_tasks, save_tasks


VALID_STATUSES = ("todo", "in-progress", "done")


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _clean_description(description: str) -> str:
    cleaned = description.strip()
    if not cleaned:
        raise ValueError("Task description cannot be empty.")
    return cleaned


def _find_task(tasks: list[dict[str, Any]], task_id: int) -> dict[str, Any] | None:
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None


def add_task(description: str) -> dict[str, Any]:
    tasks = load_tasks()
    now = _timestamp()

    task = {
        "id": get_next_task_id(tasks),
        "description": _clean_description(description),
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def update_task(task_id: int, description: str) -> dict[str, Any]:
    tasks = load_tasks()
    task = _find_task(tasks, task_id)
    if task is None:
        raise ValueError(f"Task with ID {task_id} not found.")

    task["description"] = _clean_description(description)
    task["updatedAt"] = _timestamp()
    save_tasks(tasks)
    return task


def delete_task(task_id: int) -> dict[str, Any]:
    tasks = load_tasks()
    task = _find_task(tasks, task_id)
    if task is None:
        raise ValueError(f"Task with ID {task_id} not found.")

    remaining_tasks = [entry for entry in tasks if entry.get("id") != task_id]
    save_tasks(remaining_tasks)
    return task


def mark_task(task_id: int, status: str) -> dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'.")

    tasks = load_tasks()
    task = _find_task(tasks, task_id)
    if task is None:
        raise ValueError(f"Task with ID {task_id} not found.")

    task["status"] = status
    task["updatedAt"] = _timestamp()
    save_tasks(tasks)
    return task


def list_tasks(status: str | None = None) -> list[dict[str, Any]]:
    tasks = load_tasks()
    if status is None:
        return sorted(tasks, key=lambda task: task.get("id", 0))

    if status == "not-done":
        return sorted(
            [task for task in tasks if task.get("status") in ("todo", "in-progress")],
            key=lambda task: task.get("id", 0),
        )

    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'.")

    return sorted(
        [task for task in tasks if task.get("status") == status],
        key=lambda task: task.get("id", 0),
    )
