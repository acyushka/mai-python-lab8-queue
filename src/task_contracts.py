from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from src.task import Task


@runtime_checkable
class TaskSource(Protocol):
    """Контракт источника задач"""

    def get_tasks(self) -> Iterable[Task]:
        """Получить итерируемую коллекцию задач из источника"""
        ...
