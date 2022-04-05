import pytest
from src.hw2.curry import curry_explicit, uncurry_explicit

def test_curry():
    function = lambda x, y, z: x + y - z
    curried_function = curry_explicit((lambda x, y, z: x + y - z), 3)
    assert curried_function(1)(3)(5) == function(1, 3, 5)


def test_uncurry():
    function = lambda x, y, z: x + y - z
    curried_function = curry_explicit(function, 3)
    uncurried_function = uncurry_explicit(curried_function, 3)
    assert uncurried_function(1, 3, 5) == function(1, 3, 5)


def test_curry_uncurry():
    curried_function = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)
    uncurried_function = uncurry_explicit(curried_function, 3)
    assert curried_function(123)(456)(562) == uncurried_function(123, 456, 562)


def test_arbitrary_arity_freezing():
    print_curried = curry_explicit(print, 2)
    assert print_curried(1)(2) is None


def test_print_currying(capfd):
    print_curried = curry_explicit(print, 3)
    print_curried("qwe")("rty")("uiop")
    out, _ = capfd.readouterr()
    assert out == "qwe rty uiop\n"


def test_curry_zero_arity():
    function = lambda: "123"
    curried_function = curry_explicit(function, 0)
    assert curried_function == function


def test_uncurry_zero_arity():
    function = lambda: "123"
    curried_function = curry_explicit(function, 0)
    uncurried_function = uncurry_explicit(curried_function, 0)
    assert uncurried_function == function


def test_curry_uncurry_zero_arity():
    function = lambda: "123"
    curried_function = curry_explicit(function, 0)
    uncurried_function = uncurry_explicit(curried_function, 0)
    assert curried_function == uncurried_function


def test_curry_one_arity():
    function = lambda x: str(x)
    curried_function = curry_explicit(function, 1)
    assert curried_function == function


def test_uncurry_one_arity():
    function = lambda x: str(x)
    curried_function = curry_explicit(function, 1)
    uncurried_function = uncurry_explicit(curried_function, 1)
    assert uncurried_function == function


def test_curry_uncurry_one_arity():
    function = lambda x: str(x)
    curried_function = curry_explicit(function, 1)
    uncurried_function = uncurry_explicit(curried_function, 1)
    assert curried_function == uncurried_function
