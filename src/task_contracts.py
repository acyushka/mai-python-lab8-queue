from typing import Protocol, runtime_checkable

from src.task import Task


@runtime_checkable
class TaskSource(Protocol):
    """Контракт источника задач"""

    def get_tasks(self) -> list[Task]:
        """Получить список задач из источника"""
        ...
