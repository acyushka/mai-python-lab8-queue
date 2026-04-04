from datetime import datetime, timezone
from typing import Any


class TaskException(Exception):
    """Базовое исключение модели"""


class TaskValidationException(TaskException):
    """Вызывается при ошибке валидации атрибутов таски"""


class InvalidStatusTransitionException(TaskException):
    """Вызывается при недопустимом изменении статуса"""


class BaseDataDescriptor:
    """Data-descriptor, валидирующий значение перед сохранением."""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: type | None = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any) -> None:
        validated = self.validate(value)
        setattr(instance, self.private_name, validated)

    def validate(self, value: Any) -> Any:
        return value


class IdDescriptor(BaseDataDescriptor):
    """Дескриптор для валидации и нормализации ID таски"""

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TaskValidationException("ID must be a string")
        normalized = value.strip()
        if not normalized:
            raise TaskValidationException("ID cannot be empty")
        return normalized


class DescriptionDescriptor(BaseDataDescriptor):
    """Дескриптор для валидации и нормализации описания таски"""

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TaskValidationException("Description must be a string")
        normalized = value.strip()
        if not normalized:
            raise TaskValidationException("Description cannot be empty")
        return normalized


class PriorityDescriptor(BaseDataDescriptor):
    """Дескриптор для валидации приоритета таски"""

    def __init__(self, min_value: int = 1, max_value: int = 5) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> int:
        if not isinstance(value, int):
            raise TaskValidationException("Priority must be an int")
        if not (self.min_value <= value <= self.max_value):
            raise TaskValidationException(
                f"Priority must be in range [{self.min_value}, {self.max_value}]"
            )
        return value


class StatusDescriptor(BaseDataDescriptor):
    """Дескриптор для валидации статуса таски"""

    def __init__(self, allowed_statuses: set[str]) -> None:
        self.allowed_statuses = allowed_statuses

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TaskValidationException("Status must be a string")
        normalized = value.strip().lower()
        if normalized not in self.allowed_statuses:
            raise TaskValidationException(
                f"invalid status: {normalized}. allowed: {sorted(self.allowed_statuses)}"
            )
        return normalized


class Task:
    """Модель задачи с валидацией атрибутов через дескрипторы"""

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_BLOCKED = "blocked"
    STATUS_DONE = "done"

    ALLOWED_STATUSES = {
        STATUS_NEW,
        STATUS_IN_PROGRESS,
        STATUS_BLOCKED,
        STATUS_DONE,
    }

    ALLOWED_TRANSITIONS = {
        STATUS_NEW: {STATUS_IN_PROGRESS, STATUS_BLOCKED},
        STATUS_IN_PROGRESS: {STATUS_DONE, STATUS_BLOCKED},
        STATUS_BLOCKED: {STATUS_IN_PROGRESS},
        STATUS_DONE: set(),
    }

    id = IdDescriptor()
    description = DescriptionDescriptor()
    priority = PriorityDescriptor(min_value=1, max_value=5)
    status = StatusDescriptor(allowed_statuses=ALLOWED_STATUSES)

    def __init__(
        self,
        id: str,
        description: str = "Untitled",
        priority: int = 3,
        status: str = STATUS_NEW,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = created_at or datetime.now(timezone.utc)

    @property
    def created_at(self) -> datetime:
        """Время создания таски (только чтение)"""
        return self._created_at

    @property
    def is_ready(self) -> bool:
        """Таска готова, если она не заблокирована и не завершена"""
        return self.status in {self.STATUS_NEW, self.STATUS_IN_PROGRESS}

    def change_status(self, new_status: str) -> None:
        """Изменяет статус таски с проверкой допустимости перехода"""

        if not isinstance(new_status, str):
            raise TaskValidationException("new status must be a string")

        normalized = new_status.strip().lower()
        if normalized not in self.ALLOWED_STATUSES:
            raise TaskValidationException(
                f"invalid status: {normalized}. allowed: {sorted(self.ALLOWED_STATUSES)}"
            )

        if normalized == self.status:
            return

        allowed = self.ALLOWED_TRANSITIONS[self.status]
        if normalized not in allowed:
            raise InvalidStatusTransitionException(
                f"transition {self.status} -> {normalized} is not allowed"
            )

        self.status = normalized

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, description={self.description!r}, "
            f"priority={self.priority}, status={self.status!r}, "
            f"created_at={self.created_at.isoformat()!r})"
        )
