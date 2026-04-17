from collections.abc import Iterator

import pytest

from src.task import Task
from src.task_queue import TaskQueue


def test_queue_supports_iteration_protocol() -> None:
    queue = TaskQueue([Task(id="1"), Task(id="2")])

    iterator = iter(queue)

    assert isinstance(iterator, Iterator)
    assert [task.id for task in queue] == ["1", "2"]


def test_queue_supports_multiple_passes() -> None:
    queue = TaskQueue([Task(id="a"), Task(id="b")])

    first_pass = [task.id for task in queue]
    second_pass = [task.id for task in queue]

    assert first_pass == ["a", "b"]
    assert second_pass == ["a", "b"]


def test_filter_by_status_is_lazy_generator() -> None:
    queue = TaskQueue(
        [
            Task(id="1", status=Task.STATUS_NEW),
            Task(id="2", status=Task.STATUS_DONE),
            Task(id="3", status=Task.STATUS_NEW),
        ]
    )

    lazy_items = queue.filter_by_status(Task.STATUS_NEW)

    assert isinstance(lazy_items, Iterator)
    assert [task.id for task in lazy_items] == ["1", "3"]


def test_filter_by_priority_is_lazy_generator() -> None:
    queue = TaskQueue(
        [
            Task(id="1", priority=1),
            Task(id="2", priority=3),
            Task(id="3", priority=5),
        ]
    )

    lazy_items = queue.filter_by_priority(min_priority=2, max_priority=4)

    assert isinstance(lazy_items, Iterator)
    assert [task.id for task in lazy_items] == ["2"]


def test_filter_ready_returns_only_ready_tasks() -> None:
    queue = TaskQueue(
        [
            Task(id="1", status=Task.STATUS_NEW),
            Task(id="2", status=Task.STATUS_IN_PROGRESS),
            Task(id="3", status=Task.STATUS_BLOCKED),
            Task(id="4", status=Task.STATUS_DONE),
        ]
    )

    assert [task.id for task in queue.filter_by_ready()] == ["1", "2"]


def test_queue_works_with_large_amount_of_tasks() -> None:
    queue = TaskQueue(Task(id=str(index)) for index in range(10000))

    total = sum(1 for _ in queue)

    assert total == 10000


def test_stop_iteration_is_handled_correctly() -> None:
    queue = TaskQueue([Task(id="only")])
    iterator = iter(queue)

    first = next(iterator)
    assert first.id == "only"

    with pytest.raises(StopIteration):
        next(iterator)


def test_add_rejects_non_task_value() -> None:
    queue = TaskQueue()

    with pytest.raises(TypeError):
        queue.add("bad")
