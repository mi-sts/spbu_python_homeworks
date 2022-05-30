import pytest
import re
import time
from src.test_2.function_logger_decorator import logger


@pytest.fixture
def temp_file_path(tmp_path) -> str:
    filename = f"{time.time()}.txt"
    temp_dir = tmp_path / "test_function_logger_decorator"
    temp_dir.mkdir()
    temp_file_path = temp_dir / filename

    return str(temp_file_path)


def _get_non_datetime_func_fields(field: str) -> str:
    non_datetime_fields = field[20:]
    non_datetime_fields = non_datetime_fields.strip("\n")
    return non_datetime_fields


def test_correct_logging_datetime_format(temp_file_path: str):
    @logger(temp_file_path)
    def func():
        return 1

    func()

    logging_file = open(temp_file_path, "r")

    assert re.match("\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.*", logging_file.read())


def test_returned_value(temp_file_path: str):
    @logger(temp_file_path)
    def func():
        return 1

    func()

    logging_file = open(temp_file_path, "r")
    logged_field = logging_file.readline()

    assert _get_non_datetime_func_fields(logged_field) == "func () () 1"


def test_several_calls(temp_file_path: str):
    @logger(temp_file_path)
    def func(a, b, c=1, d=2):
        return [a, b, c, d]

    func(1, 2)
    func(3, 4, c=5, d=6)

    logging_file = open(temp_file_path, "r")
    first_field, second_field = logging_file.readlines()

    assert (
        _get_non_datetime_func_fields(first_field) == "func (1, 2) () [1, 2, 1, 2]"
        and _get_non_datetime_func_fields(second_field) == "func (3, 4) ('c': 5, 'd': 6) [3, 4, 5, 6]"
    )


def test_no_return_func(temp_file_path):
    @logger(temp_file_path)
    def func():
        print(1)

    func()

    logging_file = open(temp_file_path, "r")
    logged_field = logging_file.readline()

    assert _get_non_datetime_func_fields(logged_field) == "func () () None"
