import pytest

from contemplation import CallCounter, ExecutionTimer, FunctionLogger, FunctionEvent


@pytest.fixture
def call_counter():
    return CallCounter()


@pytest.fixture
def execution_timer():
    return ExecutionTimer()


@pytest.fixture
def function_logger():
    return FunctionLogger()


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


def test_function_logger(function_logger: FunctionLogger):
    @function_logger.log_function()
    def my_func(a: int, b: int):
        return a + b

    for i in range(100):
        my_func(i, i + 1)

    assert len(function_logger.get_logs()) == 100

    @function_logger.log_function()
    def my_func_v2(a: int, b: int):
        return a + b

    for i in range(50):
        my_func_v2(i, i + 1)

    assert len(function_logger.get_logs()) == 150

    assert len(function_logger.get_logs_by_function_name("my_func")) == 100
    assert len(function_logger.get_logs_by_function_name("my_func_v2")) == 50
    assert len(function_logger.get_logs_by_function_name("my_func_v3")) == 0


def test_function_event():
    fe = FunctionEvent("my_func", 1, 2, None, None)

    fe_dict = fe.to_dict()

    assert fe_dict["name"] == "my_func"
    assert fe_dict["start_time"] == 1
    assert fe_dict["end_time"] == 2
    assert fe_dict["duration"] == 1
    assert fe.duration == 1


def test_function_log_iteration(function_logger: FunctionLogger):
    @function_logger.log_function()
    def my_func(a: int, b: int):
        return a + b

    for i in range(100):
        my_func(i, i + 1)

    c = 0
    for log in function_logger:
        assert isinstance(log, FunctionEvent)
        c += 1

    assert c == 100
