import pytest

from src.task import Task


def test_task_create_with_valid_data():
    task = Task(id="1", payload={"value": 10})

    assert task.id == "1"
    assert task.payload == {"value": 10}


def test_task_payload_default_is_empty_dict():
    task = Task(id="2")

    assert task.payload == {}


def test_task_raises_for_empty_id():
    with pytest.raises(ValueError):
        Task(id="", payload={})


def test_task_raises_for_non_dict_payload():
    with pytest.raises(TypeError):
        Task(id="3", payload=[1, 2, 3])
