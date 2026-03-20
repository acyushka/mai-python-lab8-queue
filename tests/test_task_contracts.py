from src.task_contracts import TaskSource
from src.task_sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource


def test_generator_source_matches_protocol_runtime():
    assert isinstance(GeneratorTaskSource(count=1), TaskSource)


def test_file_source_matches_protocol_runtime():
    assert isinstance(FileTaskSource(filepath="dummy.json"), TaskSource)


def test_api_source_matches_protocol_runtime():
    assert isinstance(ApiTaskSource(), TaskSource)


class BadSource:
    pass


def test_bad_source_not_match_protocol_runtime():
    assert not isinstance(BadSource(), TaskSource)
