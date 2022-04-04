import pytest
import time
from threading import Thread
from src.hw3.dict_semaphore import LockDict


def test_safe_access():
    def long_calculation(value: int) -> int:
        time.sleep(0.001)
        return value

    def add_to_counter(locked_dictionary: dict, value: int):
        with locked_dictionary as ld:
            ld["counter"] += long_calculation(value)

    dictionary = {"counter": 0}
    locked_dictionary = LockDict(dictionary)
    threads = []
    for i in range(1000):
        increasing_thread = Thread(target=add_to_counter, args=(locked_dictionary, 100))
        decreasing_thread = Thread(target=add_to_counter, args=(locked_dictionary, -100))
        threads.append(increasing_thread)
        threads.append(decreasing_thread)
        increasing_thread.start()
        decreasing_thread.start()

    map(lambda t: t.join(), threads)
    assert dictionary["counter"] == 0


def test_initial_dictionary_elements():
    initial_dictionary = {"1": 1, "2": 2, "3": 3}
    with LockDict(initial_dictionary) as ld:
        ld["4"] = 4
        ld["5"] = 5
        ld["1"] = -1
    assert initial_dictionary == {"1": -1, "2": 2, "3": 3, "4": 4, "5": 5}


def test_not_with_access_safety():
    dictionary = {"1": 1}
    locked_dictionary = LockDict(dictionary)
    try:
        locked_dictionary["1"] = 2
    finally:
        assert dictionary == {"1": 1}