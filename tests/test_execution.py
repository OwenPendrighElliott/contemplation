import pytest

from contemplation import (
    CallCounter,
    ExecutionTimer,
)


@pytest.fixture
def call_counter():
    return CallCounter()


@pytest.fixture
def execution_timer():
    return ExecutionTimer()


def test_call_counter(call_counter: CallCounter):
    @call_counter.count_calls
    def my_func(a: int, b: int):
        return a + b

    for i in range(100):
        my_func(i, i + 1)

    assert call_counter.get_count(my_func) == 100
    assert len(call_counter.get_counts()) == 1

    @call_counter.count_calls
    def my_func_v2(a: int, b: int):
        return a + b

    for i in range(50):
        my_func_v2(i, i + 1)

    assert call_counter.get_count(my_func_v2) < 100.0
    assert len(call_counter.get_counts()) == 2
    assert call_counter.get_count(my_func_v2) > 0.0

    assert call_counter.get_count("my_func") > 0.0
    assert call_counter.get_count("my_func_v2") > 0.0


def test_execution_timer(execution_timer: ExecutionTimer):
    @execution_timer.time_execution
    def my_func(a: int, b: int):
        return a + b

    for i in range(100):
        my_func(i, i + 1)

    assert execution_timer.get_execution_time(my_func) < 100.0
    assert len(execution_timer.get_execution_times()) == 1
    assert execution_timer.get_execution_time(my_func) > 0.0

    @execution_timer.time_execution
    def my_func_v2(a: int, b: int):
        return a + b

    for i in range(50):
        my_func_v2(i, i + 1)

    assert execution_timer.get_execution_time(my_func_v2) < 100.0
    assert len(execution_timer.get_execution_times()) == 2
    assert execution_timer.get_execution_time(my_func_v2) > 0.0

    assert execution_timer.get_execution_time("my_func") > 0.0
    assert execution_timer.get_execution_time("my_func_v2") > 0.0
