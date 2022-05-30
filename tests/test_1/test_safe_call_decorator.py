import pytest
import time
import pathlib
from src.test_1.safe_call_decorator import safe_call


@pytest.fixture
def temp_file_path(tmp_path) -> pathlib.Path:
    filename = f"{time.time()}.txt"
    temp_dir = tmp_path / "test_bush_imitating_functions"
    temp_dir.mkdir()
    temp_file_path = temp_dir / filename

    return temp_file_path


def _read_file_text(file_path: pathlib.Path) -> str:
    file = open(file_path)
    text = file.read()
    file.close()

    return text


def test_safe_call_without_exception_return_value(temp_file_path):
    temp_file = open(temp_file_path, "w")

    @safe_call(temp_file)
    def func():
        return 1

    assert func() == 1


def test_safe_call_without_exception_empty_file(temp_file_path):
    temp_file_writing = open(temp_file_path, "w")

    @safe_call(temp_file_writing)
    def func():
        return 1

    func()
    assert _read_file_text(temp_file_path) == ""


def test_safe_call_zero_division_logging(temp_file_path):
    temp_file_writing = open(temp_file_path, "w")

    @safe_call(temp_file_writing)
    def func():
        return 1 / 0

    func()
    temp_file_lines = _read_file_text(temp_file_path).split("\n")

    assert (
        temp_file_lines[0][:9] == "Function:"
        and temp_file_lines[1] == "args: (), kwargs: {}"
        and temp_file_lines[2] == "Exception: ZeroDivisionError('division by zero')"
    )


def test_safe_call_args_kwargs_logging(temp_file_path):
    temp_file_writing = open(temp_file_path, "w")

    @safe_call(temp_file_writing)
    def func(a, b, *args, **kwargs):
        return a * b

    func("first", "second", "third", "fourth", c="fifth", d=6)
    temp_file_lines = _read_file_text(temp_file_path).split("\n")

    assert temp_file_lines[1] == "args: ('first', 'second', 'third', 'fourth'), kwargs: {'c': 'fifth', 'd': 6}"
