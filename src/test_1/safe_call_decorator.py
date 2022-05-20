from typing import Callable, IO
import functools


def safe_call(file: IO):
    def _get_logging_text(func: Callable, args, kwargs, exception: Exception) -> str:
        return f"Function: {repr(func)}\nargs: {args}, kwargs: {kwargs}\nException: {repr(exception)}\n"

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func_result = func(*args, **kwargs)
                return func_result
            except Exception as exception:
                file.write(_get_logging_text(func, args, kwargs, exception))
                return None

        return wrapper

    return decorator
