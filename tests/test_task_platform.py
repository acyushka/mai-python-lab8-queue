import pytest

from src.task import Task
from src.task_platform import TaskPlatform


class SimpleTaskSource:
    def __init__(self, tasks: list[Task]):
        self._tasks = tasks

    def get_tasks(self):
        return (task for task in self._tasks)


class InvalidSource:
    pass


def test_platform_adds_valid_source_and_counts():
    platform = TaskPlatform()

    platform.add_source(SimpleTaskSource([Task(id="a")]))

    assert platform.source_count == 1


def test_platform_rejects_invalid():
    platform = TaskPlatform()

    with pytest.raises(TypeError):
        platform.add_source(InvalidSource())


def test_platform_rejects_duplicate():
    platform = TaskPlatform()
    source = SimpleTaskSource([Task(id="a")])

    platform.add_source(source)

    with pytest.raises(ValueError):
        platform.add_source(source)


def test_platform_collects_tasks_from_all_sources():
    platform = TaskPlatform()
    source_one = SimpleTaskSource([Task(id="1"), Task(id="2")])
    source_two = SimpleTaskSource([Task(id="3")])

    platform.add_source(source_one)
    platform.add_source(source_two)

    tasks = platform.collect_all_tasks()

    assert [task.id for task in tasks] == ["1", "2", "3"]


def test_platform_queues_tasks_successfully():
    platform = TaskPlatform()
    source_one = SimpleTaskSource([Task(id="1"), Task(id="2")])
    source_two = SimpleTaskSource([Task(id="3")])

    platform.add_source(source_one)
    platform.add_source(source_two)

    streamed_tasks = [task.id for task in platform.queue_all_tasks()]

    assert streamed_tasks == ["1", "2", "3"]
