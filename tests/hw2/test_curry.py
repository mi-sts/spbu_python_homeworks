import pytest
from src.hw2.curry import curry_explicit, uncurry_explicit


def test_curry_uncurry():
    f2 = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)
    g2 = uncurry_explicit(f2, 3)
    expected_string = "<123,456,562>"
    assert f2(123)(456)(562) == expected_string
    assert g2(123, 456, 562) == expected_string


def test_arbitrary_arity_freezing():
    print_curried = curry_explicit(print, 2)
    assert print_curried(1)(2) is None


def test_print_currying(capfd):
    print_curried = curry_explicit(print, 3)
    print_curried("qwe")("rty")("uiop")
    out, _ = capfd.readouterr()
    assert out == "qwe rty uiop\n"


def test_curry_uncurry_zero_arity():
    f = lambda: "123"
    f_curried = curry_explicit(f, 0)
    f_uncurried = uncurry_explicit(f_curried, 0)
    assert f_curried == f
    assert f_uncurried == f


def test_curry_uncurry_one_arity():
    f = lambda x: str(x)
    f_curried = curry_explicit(f, 1)
    f_uncurried = uncurry_explicit(f_curried, 1)
    assert f_curried == f
    assert f_uncurried == f
