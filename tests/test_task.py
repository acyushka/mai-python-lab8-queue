from datetime import datetime, timezone

import pytest

from src.task import (
    InvalidStatusTransitionException,
    Task,
    TaskValidationException,
)


def test_task_create_with_valid_data() -> None:
    task = Task(
        id=" 1 ",
        description=" Implement API ",
        priority=4,
        status=Task.STATUS_NEW,
    )

    assert task.id == "1"
    assert task.description == "Implement API"
    assert task.priority == 4
    assert task.status == Task.STATUS_NEW
    assert task.is_ready is True
    assert isinstance(task.created_at, datetime)


def test_task_created_at_read_only() -> None:
    task = Task(id="2", description="Read-only timestamp")

    with pytest.raises(AttributeError):
        task.created_at = datetime.now(timezone.utc)


def test_task_raises_for_empty_id() -> None:
    with pytest.raises(TaskValidationException):
        Task(id=" ", description="x")


def test_task_raises_for_empty_description() -> None:
    with pytest.raises(TaskValidationException):
        Task(id="1", description=" ")


def test_task_raises_for_invalid_priority() -> None:
    with pytest.raises(TaskValidationException):
        Task(id="1", description="x", priority=10)


def test_task_raises_for_invalid_status() -> None:
    with pytest.raises(TaskValidationException):
        Task(id="1", description="x", status="unknown")


def test_valid_status_transition() -> None:
    task = Task(id="1", description="x", status=Task.STATUS_NEW)

    task.change_status(Task.STATUS_IN_PROGRESS)
    task.change_status(Task.STATUS_DONE)

    assert task.status == Task.STATUS_DONE
    assert task.is_ready is False


def test_invalid_status_transition_raises() -> None:
    task = Task(id="1", description="x", status=Task.STATUS_NEW)

    with pytest.raises(InvalidStatusTransitionException):
        task.change_status(Task.STATUS_DONE)
