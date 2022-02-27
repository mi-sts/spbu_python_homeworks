import pytest
from src.hw1.vector import *


@pytest.mark.parametrize("first", "second", "expected", [
    (Vector(1, 2), Vector(2, 3), Vector(3, 5)),
    (Vector(0, 0), Vector(0, 0), Vector(0, 0)),
    (Vector(-3, 2), Vector(3, -2), Vector(0, 0)),
    (Vector(4, -5), Vector(-2, 4), Vector(2, -1)),

    (Vector(1, 2, 3), Vector(4, 5, 6), Vector(5, 7, 9)),
    (Vector(5), Vector(2), Vector(7)),

    (Vector(0.0, 0.0), Vector(0.0, 0.0), Vector(0.0, 0.0)),
    (Vector(0.5, -2.0), Vector(1.5, 0.5), Vector(2.0, -1.5)),
])
def test_add(first, second, expected):
    assert first + second == expected

# def test_sub()
