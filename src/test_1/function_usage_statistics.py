from typing import Callable


def spy(function: Callable):
    from datetime import datetime

    def usage_statistics_generator() -> tuple:
        for i in usage_statistics:
            yield i

    usage_statistics = []

    def wrapper(*args, **kwargs) -> object:
        function_return = function(*args, **kwargs)
        usage_statistics.append((datetime.now(), (*args, *kwargs)))
        return function_return

    wrapper.statistics_generator = usage_statistics_generator

    return wrapper


def print_usage_statistic(function: Callable) -> object:
    try:
        return function.statistics_generator()
    except AttributeError:
        print("This function is not decorated with spy!")
