import test
from src.test_1.function_usage_statistics import spy
from src.test_1.function_usage_statistics import print_usage_statistic


def test_print_usage_datetime():
    @spy
    def foo(num):
        print(num)

    @spy
    def boo(first_num, second_num):
        print(first_num, second_num)

    for i in range(3):
        foo(i)

    for i in range(2):
        for j in range(2):
            boo(i, j)

    foo_statistics = print_usage_statistic(foo)
    boo_statistics = print_usage_statistic(boo)

    foo_args = [i[1] for i in foo_statistics]
    boo_args = [i[1] for i in boo_statistics]

    assert foo_args == [(0,), (1,), (2,)]
    assert boo_args == [(0, 0), (0, 1), (1, 0), (1, 1)]

def test_wrapped_function_return():
    @spy
    def foo(num):
        return num

    assert foo(5) == 5
