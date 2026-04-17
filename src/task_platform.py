from collections.abc import Generator

from src.task import Task
from src.task_contracts import TaskSource


class TaskPlatform:
    """Платформа приема задач из нескольких источников"""

    def __init__(self) -> None:
        self._sources: list[TaskSource] = []

    def add_source(self, source: TaskSource) -> None:
        """Добавить источник задач в платформу"""
        if not isinstance(source, TaskSource):
            raise TypeError(
                f"{type(source).__name__} не реализует контракт TaskSource")

        if source in self._sources:
            raise ValueError(
                f"Источник {type(source).__name__} уже зарегистрирован")

        self._sources.append(source)

    def collect_all_tasks(self) -> list[Task]:
        """Собрать задачи из всех зарегистрированных источников"""
        all_tasks: list[Task] = []
        for source in self._sources:
            all_tasks.extend(source.get_tasks())
        return all_tasks

    def queue_all_tasks(self) -> Generator[Task, None, None]:
        """Лениво вернуть задачи"""
        for source in self._sources:
            yield from source.get_tasks()

    @property
    def source_count(self) -> int:
        """Количество зарегистрированных источников"""
        return len(self._sources)
