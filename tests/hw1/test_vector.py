import pytest
from src.hw1.vector import *


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (Vector(1, 2), Vector(2, 3), Vector(3, 5)),
        (Vector(0, 0), Vector(0, 0), Vector(0, 0)),
        (Vector(4, -5), Vector(-2, 4), Vector(2, -1)),
        (Vector(1, 2, 3), Vector(4, 5, 6), Vector(5, 7, 9)),
        (Vector(5), Vector(2), Vector(7)),
        (Vector(0.5, -2.0), Vector(1.5, 0.5), Vector(2.0, -1.5)),
        (Vector(1, 2.0), Vector(4, 2.5), Vector(5, 4.5)),
    ],
)
def test_add(first, second, expected):
    assert first + second == expected


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (Vector(1, 2), Vector(2, 3), Vector(-1, -1)),
        (Vector(0, 0), Vector(0, 0), Vector(0, 0)),
        (Vector(4, -5), Vector(-2, 4), Vector(6, -9)),
        (Vector(1, 2, 3), Vector(4, 5, 6), Vector(-3, -3, -3)),
        (Vector(5), Vector(2), Vector(3)),
        (Vector(0.5, -2.0), Vector(1.5, 0.5), Vector(-1.0, -2.5)),
        (Vector(1, 2.0), Vector(4, 2.5), Vector(-3, -0.5)),
    ],
)
def test_sub(first, second, expected):
    assert first - second == expected


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (Vector(1, 2), Vector(2, 3), 8),
        (Vector(0, 0), Vector(0, 0), 0),
        (Vector(4, -5), Vector(-2, 4), -28),
        (Vector(1, 2, 3), Vector(4, 5, 6), 32),
        (Vector(5), Vector(2), 10),
        (Vector(0.5, -2.0), Vector(1.5, 0.5), -0.25),
        (Vector(1, 2.0), Vector(4, 2.5), 9.0),
        (Vector(1, 2), 2, Vector(2, 4)),
        (Vector(1, 2), 2.5, Vector(2.5, 5.0)),
        (2, Vector(3, 4), Vector(6, 8)),
        (Vector(2.5, 3), 4, Vector(10.0, 12.0)),
        (Vector(1, 3, 5), 2, Vector(2, 6, 10)),
    ],
)
def test_mul(first, second, expected):
    assert first * second == expected


@pytest.mark.parametrize(
    "vector, module",
    [
        (Vector(1, 2), math.sqrt(5)),
        (Vector(0, 0), 0),
        (Vector(4, -5), math.sqrt(41)),
        (Vector(1, 2, 3), math.sqrt(14)),
        (Vector(5), 5.0),
        (Vector(0.5, -2.0), math.sqrt(4.25)),
        (Vector(1, 2.0), math.sqrt(5.0)),
    ],
)
def test_module(vector, module):
    assert vector.module() == module


@pytest.mark.parametrize(
    "first, second, angle",
    [
        (Vector(1, 0), Vector(0, 1), math.pi / 2),
        (Vector(1, 1), Vector(2, 2), 0.0),
        (Vector(5), Vector(2), 0.0),
        (Vector(1, 2), Vector(1, 2), 0.0),
        (Vector(1.0, 2.0), Vector(1.0, 2.0), 0.0),
        (Vector(1, 1), Vector(1.5, 1.5), 0.0),
        (Vector(1, 0), Vector(1, 1), math.pi / 4),
    ],
)
def test_angle(first, second, angle):
    assert round(first.angle(second), 7) == round(angle, 7)


@pytest.mark.parametrize(
    "first, second", [(Vector(0, 0), Vector(0, 0)), (Vector(1, 1), Vector(0, 0))]
)
def test_not_defined_angle(first, second):
    assert first.angle(second) is None
