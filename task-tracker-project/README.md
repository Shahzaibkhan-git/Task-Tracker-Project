# Task Tracker CLI

A simple command-line task tracker built with pure Python and no external libraries.

## Features

- Add, update, and delete tasks
- Mark tasks as `in-progress` or `done`
- List all tasks
- List tasks by status: `todo`, `in-progress`, `done`
- List tasks that are not done: `not-done`
- Store tasks in a local JSON file (`tasks.json`)

## Project Structure

```text
task-tracker-project/
├── task-cli
├── task_service.py
├── task_store.py
├── tasks.json
└── README.md
```

## Requirements

- Python 3.10+ (standard library only)

## Usage

Run from the project directory:

```bash
cd task-tracker-project
python3 task-cli <action> [params...]
```

If you want to run `./task-cli ...` directly, make it executable first:

```bash
chmod +x task-cli
```

## Commands

```bash
# Add a task
python3 task-cli add "Buy groceries"

# Update and delete
python3 task-cli update 1 "Buy groceries and cook dinner"
python3 task-cli delete 1

# Mark status
python3 task-cli mark-in-progress 1
python3 task-cli mark-done 1

# List tasks
python3 task-cli list
python3 task-cli list done
python3 task-cli list todo
python3 task-cli list in-progress
python3 task-cli list not-done
```

## Task Object

Each task has:

- `id`: unique integer ID
- `description`: task text
- `status`: `todo`, `in-progress`, or `done`
- `createdAt`: creation timestamp (ISO format)
- `updatedAt`: last update timestamp (ISO format)

## Notes

- `tasks.json` is created automatically if missing.
- Invalid commands, IDs, and statuses are handled with clear error messages.
- Use `task-cli` (hyphen), not `task_cli` (underscore).
