#!/usr/bin/env python3
"""Simple command-line todo manager.

Usage examples:
    python todo.py add "Buy milk"
    python todo.py list
    python todo.py done 1
    python todo.py delete 1
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).with_name("todos.json")


def load_tasks() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)
        file.write("\n")


def add_task(description: str) -> None:
    tasks = load_tasks()
    tasks.append({"id": len(tasks) + 1, "description": description, "done": False})
    save_tasks(tasks)
    print(f"Added task #{tasks[-1]['id']}: {description}")


def list_tasks() -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        status = "✓" if task.get("done") else " "
        print(f"{task['id']}. [{status}] {task['description']}")


def complete_task(task_id: int) -> None:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Marked task #{task_id} as done.")
            return

    print(f"Task #{task_id} not found.")


def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    updated = [task for task in tasks if task["id"] != task_id]
    if len(updated) == len(tasks):
        print(f"Task #{task_id} not found.")
        return

    for index, task in enumerate(updated, start=1):
        task["id"] = index

    save_tasks(updated)
    print(f"Deleted task #{task_id}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple todo manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new todo item")
    add_parser.add_argument("description", help="Task description")

    subparsers.add_parser("list", help="List all todo items")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark complete")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.task_id)
    elif args.command == "delete":
        delete_task(args.task_id)


if __name__ == "__main__":
    main()
