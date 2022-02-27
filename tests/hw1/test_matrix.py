import pytest
from src.hw1.matrix import Matrix


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (
                ((1, 2),
                 (2, 3)),

                ((4, 5),
                 (5, 6)),

                ((5, 7),
                 (7, 9)),
        ),
        (
                ((-5, 3),
                 (1.5, -2)),

                ((2, 2.5),
                 (0, 6)),

                ((-3, 5.5),
                 (1.5, 4)),
        ),
        (
                ((-1, 2),
                 (3, -4),
                 (-5, 6)),

                ((7, -8),
                 (-9, 10),
                 (11, -12)),

                ((6, -6),
                 (-6, 6),
                 (6, -6))
        )
    ]
)
def test_add(first, second, expected):
    assert Matrix(first) + Matrix(second) == Matrix(expected)

@pytest.mark.parametrize(
    "first, second, expected",
    [
        (
                ((1, 2),
                 (2, 3)),

                ((4, 5),
                 (5, 6)),

                ((-3, -3),
                 (-3, -3)),
        ),
        (
                ((-5, 3),
                 (1.5, -2)),

                ((2, 2.5),
                 (0, 6)),

                ((-7, 0.5),
                 (1.5, -8)),
        ),
        (
                ((-1, 2),
                 (3, -4),
                 (-5, 6)),

                ((7, -8),
                 (-9, 10),
                 (11, -12)),

                ((-8, 10),
                 (12, -14),
                 (-16, 18))
        )
    ]
)
def test_sub(first, second, expected):
    assert Matrix(first) - Matrix(second) == Matrix(expected)


@pytest.mark.parametrize(
    "matrix, transposed",
    [
        (
                ((1, 2),
                 (3, 4)),

                ((1, 3),
                 (2, 4))
        ),
        (
                ((-5, 3),
                 (1.5, -2)),

                ((-5, 1.5),
                 (3, -2))
        ),
        (
                ((-1, 2),
                 (3, -4),
                 (-5, 6)),

                ((-1, 3, -5),
                 (2, -4, 6))
        ),
        (
                ((1,),),
                ((1,),),
        )
    ]
)
def test_transposed(matrix, transposed):
    assert Matrix(matrix).transposed() == Matrix(transposed)

@pytest.mark.parametrize(
    "first, second, expected",
    [
        (
                ((1, 2),
                 (2, 3)),

                2,

                ((2, 4),
                 (4, 6)),
        ),
        (
                2.5,

                ((-2, 4),
                 (2, -3)),

                ((-5, 10),
                 (5, -7.5)),
        ),
        (
                ((1, 2, 3, 4),
                 (5, 6, 7, 8)),

                ((9, 8),
                 (7, 6),
                 (5, 4),
                 (3, 2)),

                ((50, 40),
                 (146, 120))
        ),
        (
                ((1.5, -2, 4),
                 (3, -4.5, 7),
                 (-5, 6, 0)),

                ((8, 2, -3.5),
                 (1, 2, -4),
                 (5.5, -1, 3)),

                ((32, -5, 14.75),
                 (58, -10, 28.5),
                 (-34, 2, -6.5))
        )
    ]
)
def test_multiply(first, second, expected):
    first, second, expected = map(lambda x: Matrix(x) if isinstance(x, tuple) else x, (first, second, expected))
    assert first * second == expected
