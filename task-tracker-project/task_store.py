from __future__ import annotations

import json
from pathlib import Path
from typing import Any


TASKS_FILE_NAME = "tasks.json"


def _tasks_file() -> Path:
    return Path.cwd() / TASKS_FILE_NAME


def ensure_tasks_file() -> Path:
    tasks_file = _tasks_file()
    if not tasks_file.exists():
        tasks_file.write_text("[]", encoding="utf-8")
    return tasks_file


def load_tasks() -> list[dict[str, Any]]:
    tasks_file = ensure_tasks_file()
    raw_content = tasks_file.read_text(encoding="utf-8").strip()
    if not raw_content:
        return []

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError("tasks.json contains invalid JSON.") from exc

    if not isinstance(data, list):
        raise ValueError("tasks.json is invalid. Expected a JSON array.")

    tasks: list[dict[str, Any]] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Task at index {index} is invalid. Expected an object.")
        tasks.append(item)
    return tasks


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    tasks_file = ensure_tasks_file()
    tasks_file.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def get_next_task_id(tasks: list[dict[str, Any]]) -> int:
    max_id = 0
    for task in tasks:
        task_id = task.get("id")
        if isinstance(task_id, int) and task_id > max_id:
            max_id = task_id
    return max_id + 1
