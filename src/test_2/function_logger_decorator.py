from typing import Callable
import functools
from time import gmtime, strftime


def logger(file_path: str):
    def _get_logging_text(func: Callable, args, kwargs, func_result, call_datetime: str) -> str:
        func_name = func.__name__
        kwargs_str = str(kwargs)[1:-1]
        args_str = str(args)[1:-1]
        return f"{call_datetime} {func_name} ({args_str}) ({kwargs_str}) {func_result}\n"

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            file = open(file_path, "a+")
            func_result = func(*args, **kwargs)
            call_datetime = strftime("%d/%m/%Y %H:%M:%S", gmtime())
            file.write(_get_logging_text(func, args, kwargs, func_result, call_datetime))
            file.close()

            return func_result

        return wrapper

    return decorator
