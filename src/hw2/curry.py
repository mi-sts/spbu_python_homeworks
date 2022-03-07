from typing import Callable

def curry_explicit(function: Callable, arity: int):
    if arity == 0:
        return