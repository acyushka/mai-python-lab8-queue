from collections.abc import Iterable, Iterator

from src.task import Task


class TaskQueue:
    """Коллекция задач"""

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        self._tasks: list[Task] = list(tasks) if tasks is not None else []

    def __iter__(self) -> Iterator[Task]:
        for task in self._tasks:
            yield task

    def __len__(self) -> int:
        return len(self._tasks)

    def add(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("task must be instance of Task")
        self._tasks.append(task)

    def extend(self, tasks: Iterable[Task]) -> None:
        for task in tasks:
            self.add(task)

    def filter_by_status(self, status: str) -> Iterator[Task]:
        normalized = status.strip().lower()
        return (task for task in self._tasks if task.status == normalized)

    def filter_by_priority(
        self,
        min_priority: int | None = None,
        max_priority: int | None = None,
    ) -> Iterator[Task]:
        return (
            task for task in self._tasks
            if (min_priority is None or task.priority >= min_priority)
            and (max_priority is None or task.priority <= max_priority)
        )

    def filter_by_ready(self) -> Iterator[Task]:
        return (task for task in self._tasks if task.is_ready)
