from typing import Callable


def curry_explicit(function: Callable, arity: int):
    if arity < 0:
        raise ValueError("Arity can't be negative!")

    if arity == 0 or arity == 1:
        return function

    def arguments_accumulator(*args):
        if len(args) == arity:
            return function(*args)

        return lambda next_argument: arguments_accumulator(*args, next_argument)

    return arguments_accumulator()


def uncurry_explicit(function: Callable, arity: int):
    if arity < 0:
        return ValueError("Arity can't be negative!")

    if arity == 0 or arity == 1:
        return function

    def uncurried_function(*args):
        if len(args) != arity:
            raise AttributeError("Incorrect number of arguments in the function!")

        nonlocal function
        for i in args[:-1]:
            function = function(i)

        return function(args[-1])

    return uncurried_function
