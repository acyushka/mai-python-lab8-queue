import json
import uuid
from pathlib import Path
from typing import Any

import requests

from src.constants import (
    DEFAULT_GENERATOR_PREFIX,
    HH_API_URL,
    HH_PER_PAGE,
    HH_SEARCH_TEXT,
    HTTP_TIMEOUT_SECONDS,
)
from src.task import Task


class FileTaskSource:
    """Источник задач из JSON-файла"""

    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def get_tasks(self) -> list[Task]:
        with Path(self._filepath).open("r", encoding="utf-8") as file:
            tasks: list[dict[str, Any]] = json.load(file)

        normalized_tasks: list[Task] = []
        for i, task in enumerate(tasks):
            normalized_tasks.append(self._normalize_item(task=task, index=i))
        return normalized_tasks

    @staticmethod
    def _normalize_item(task: dict[str, Any], index: int) -> Task:
        if "id" not in task.keys():
            raise ValueError(f"Task with index {index} does not contain id")

        payload_value = task.get("payload", {})
        payload = payload_value if isinstance(payload_value, dict) else {}
        return Task(id=str(task["id"]), payload=payload)

    def __repr__(self) -> str:
        return f"FileTaskSource(filepath={self._filepath!r})"


class GeneratorTaskSource:
    """Источник задач, генерируемых программно"""

    def __init__(self, count: int, prefix: str = DEFAULT_GENERATOR_PREFIX) -> None:
        self._count = count
        self._prefix = prefix

    def get_tasks(self) -> list[Task]:
        return [
            Task(
                id=f"{self._prefix}-{uuid.uuid4().hex[:8]}",
                payload={"source": "generator",
                         "generated": True, "position": index},
            )
            for index in range(self._count)
        ]

    def __repr__(self) -> str:
        return f"GeneratorTaskSource(count={self._count}, prefix={self._prefix!r})"


class ApiTaskSource:
    """Источник задач вакансий с hh.ru API"""

    def __init__(
        self,
        api_url: str = HH_API_URL,
        search_text: str = HH_SEARCH_TEXT,
        per_page: int = HH_PER_PAGE,
    ) -> None:
        self._api_url = api_url
        self._search_text = search_text
        self._per_page = per_page

    def get_tasks(self) -> list[Task]:
        params: dict[str, Any] = {
            "text": self._search_text,
            "per_page": self._per_page,
        }

        try:
            response = requests.get(
                self._api_url, params=params, timeout=HTTP_TIMEOUT_SECONDS)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        except requests.RequestException as e:
            print(f"[ApiTaskSource] Ошибка запроса к API: {e}")
            return []

        raw_items = data.get("items", [])
        if not isinstance(raw_items, list):
            return []

        tasks: list[Task] = []
        for item in raw_items:
            if not isinstance(item, dict) or "id" not in item:
                continue
            tasks.append(self._map_item_to_task(item))

        return tasks

    @staticmethod
    def _map_item_to_task(item: dict[str, Any]) -> Task:
        employer_data = item.get("employer", {})
        employer_name = None
        if isinstance(employer_data, dict):
            employer_name = employer_data.get("name")

        payload: dict[str, Any] = {
            "source": "hh_api",
            "name": item.get("name"),
            "employer": employer_name,
        }
        return Task(id=f"hh-{item['id']}", payload=payload)

    def __repr__(self) -> str:
        return (
            "ApiTaskSource("
            f"api_url={self._api_url!r}, "
            f"search_text={self._search_text!r}, "
            f"per_page={self._per_page!r}"
            ")"
        )
