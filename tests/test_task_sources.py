import json
from pathlib import Path

import pytest
import requests

from src.task import Task
from src.task_sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource


class FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def build_file_source(tmp_path: Path, payload: list[dict]) -> FileTaskSource:
    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps(payload), encoding="utf-8")
    return FileTaskSource(filepath=str(file_path))


def test_file_task_source_reads_and_normalizes_items(tmp_path):
    source = build_file_source(
        tmp_path,
        [
            {"id": 1, "description": "First", "priority": 5, "status": "new"},
            {"id": "2", "description": "", "priority": "bad", "status": 123},
        ],
    )
    tasks = source.get_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[0].description == "First"
    assert tasks[0].priority == 5
    assert tasks[0].status == Task.STATUS_NEW
    assert tasks[1].id == "2"
    assert tasks[1].description == "Untitled task"
    assert tasks[1].priority == 3
    assert tasks[1].status == Task.STATUS_NEW


def test_file_task_source_raises_when_id_missing(tmp_path: Path):
    source = build_file_source(tmp_path, [{"description": "xxx"}])

    with pytest.raises(ValueError):
        source.get_tasks()


def test_generator_source_creates_tasks():
    source = GeneratorTaskSource(count=3, prefix="demo")

    tasks = source.get_tasks()

    assert len(tasks) == 3
    assert all(task.id.startswith("demo-") for task in tasks)
    assert all(task.status == Task.STATUS_NEW for task in tasks)
    assert all(task.description.startswith("Generated task #") for task in tasks)


def test_api_source_returns_tasks_from_hh_payload(monkeypatch: pytest.MonkeyPatch):
    payload = {
        "items": [
            {
                "id": "123",
                "name": "Python Developer",
                "employer": {"name": "LLDLALDAL"},
            },
            {
                "id": "124",
                "name": "Backend Python Engineer",
                "employer": {},
            },
        ]
    }

    def fake_get(*args, **kwargs) -> FakeResponse:
        return FakeResponse(payload)

    monkeypatch.setattr(requests, "get", fake_get)
    source = ApiTaskSource()

    tasks = source.get_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == "hh-123"
    assert tasks[0].description == "Python Developer"
    assert tasks[0].priority == 2
    assert tasks[0].status == Task.STATUS_NEW


def test_api_source_returns_empty_list_on_request_error(monkeypatch: pytest.MonkeyPatch):
    def fake_get(*args, **kwargs) -> FakeResponse:
        raise requests.RequestException("boom")

    monkeypatch.setattr(requests, "get", fake_get)
    source = ApiTaskSource()

    tasks = source.get_tasks()

    assert tasks == []
