import pytest
import math
from src.hw1.vector import Vector


@pytest.mark.parametrize(
    "first, second, expected",
    [
        ((1, 2), (2, 3), (3, 5)),
        ((0, 0), (0, 0), (0, 0)),
        ((4, -5), (-2, 4), (2, -1)),
        ((1, 2, 3), (4, 5, 6), (5, 7, 9)),
        ((5,), (2,), (7,)),
        ((0.5, -2), (1.5, 0.5), (2, -1.5)),
        ((1, 2), (4, 2.5), (5, 4.5)),
    ],
)
def test_add(first, second, expected):
    assert Vector(*first) + Vector(*second) == Vector(*expected)


@pytest.mark.parametrize(
    "first, second, expected",
    [
        ((1, 2), (2, 3), (-1, -1)),
        ((0, 0), (0, 0), (0, 0)),
        ((4, -5), (-2, 4), (6, -9)),
        ((1, 2, 3), (4, 5, 6), (-3, -3, -3)),
        ((5,), (2,), (3,)),
        ((0.5, -2), (1.5, 0.5), (-1, -2.5)),
        ((1, 2), (4, 2.5), (-3, -0.5)),
    ],
)
def test_sub(first, second, expected):
    assert Vector(*first) - Vector(*second) == Vector(*expected)


@pytest.mark.parametrize(
    "first, second, expected",
    [
        ((1, 2), (2, 3), 8),
        ((0, 0), (0, 0), 0),
        ((4, -5), (-2, 4), -28),
        ((1, 2, 3), (4, 5, 6), 32),
        ((5,), (2,), 10),
        ((0.5, -2), (1.5, 0.5), -0.25),
        ((1, 2), (4, 2.5), 9),
        ((1, 2), 2, (2, 4)),
        ((1, 2), 2.5, (2.5, 5)),
        (2, (3, 4), (6, 8)),
        ((2.5, 3), 4, (10, 12)),
        ((1, 3, 5), 2, (2, 6, 10)),
    ],
)
def test_mul(first, second, expected):
    first, second, expected = map(lambda x: Vector(*x) if isinstance(x, tuple) else x, (first, second, expected))
    assert first * second == expected


@pytest.mark.parametrize(
    "coordinates, module",
    [
        ((1, 2), math.sqrt(5)),
        ((0, 0), 0),
        ((4, -5), math.sqrt(41)),
        ((1, 2, 3), math.sqrt(14)),
        ((5,), 5),
        ((0.5, -2), math.sqrt(4.25)),
        ((1, 2), math.sqrt(5)),
    ],
)
def test_module(coordinates, module):
    assert Vector(*coordinates).module() == module


@pytest.mark.parametrize(
    "first, second, angle",
    [
        ((1, 0), (0, 1), math.pi / 2),
        ((1, 1), (2, 2), 0),
        ((5,), (2,), 0),
        ((1, 2), (1, 2), 0),
        ((1, 2), (1, 2), 0),
        ((1, 1), (1.5, 1.5), 0),
        ((1, 0), (1, 1), math.pi / 4),
    ],
)
def test_angle(first, second, angle):
    assert round(Vector(*first).angle(Vector(*second)), 7) == round(angle, 7)


@pytest.mark.parametrize("first, second", [((0, 0), (0, 0)), ((1, 1), (0, 0))])
def test_not_defined_angle(first, second):
    assert Vector(*first).angle(Vector(*second)) is None
