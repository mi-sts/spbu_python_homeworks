from typing import Callable


def curry_explicit(function: Callable, arity: int):
    args = []

    def curry_func_tail(argument):
        if len(args) == arity:
            raise AttributeError("Too many arguments in function!")

        args.append(argument)
        if len(args) == arity:
            return function(*args)

        return curry_func_tail

    return curry_func_tail
