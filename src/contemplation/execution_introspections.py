from collections import defaultdict
import time
import inspect
import json
from functools import wraps
from typing import Dict, List, Callable, Union, Optional, Any


class CallCounter:
    def __init__(self):
        self.counts: Dict[str, int] = defaultdict(int)

    def count_calls(self, func: Callable) -> Callable:
        """Count the number of times a function has been called

        Args:
            func (Callable): The function to count calls for

        Returns:
            Callable: The wrapped function

        Examples:
            >>> call_counter = CallCounter()
            >>> @call_counter.count_calls
            ... def my_func(a: int, b: int):
            ...     return a + b
            >>> for i in range(100):
            ...     my_func(i, i + 1)
            >>> call_counter.get_count(my_func)
            100
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            self.counts[name] += 1
            return func(*args, **kwargs)

        return wrapper

    def get_counts(self) -> Dict[str, int]:
        """Get the counts of all functions that have been counted

        Returns:
            Dict[str, int]: A dictionary of function names to their counts
        """
        return dict(self.counts)

    def get_count(self, func: Union[Callable, str]) -> int:
        """Get the count of a specific function

        Args:
            func (Union[Callable, str]): The function to get the count for, as an instance of the function or the name of the function

        Returns:
            int: The number of times the function has been called
        """
        if isinstance(func, str):
            name = func
        else:
            name = func.__name__
        return self.counts[name]

    def pretty_print_counts(self) -> None:
        """Print the counts of all functions that have been counted"""
        name_width = max(len(name) for name in self.counts.keys())
        count_width = max(len(str(count)) for count in self.counts.values())
        name_width = max(name_width, len("Function"))
        count_width = max(count_width, len("Count"))

        print(f"{'Function':<{name_width}} | {'Count':<{count_width}}")
        print("-" * (name_width + count_width + 3))
        for name, count in self.counts.items():
            print(f"{name:<{name_width}} | {count:<{count_width}}")


class ExecutionTimer:
    def __init__(self):
        self.times = defaultdict(list)
        self.total_execution_times = defaultdict(float)

    def time_execution(self, func: Callable) -> Callable:
        """A decorator to time the execution of a function

        Args:
            func (Callable): The function to time

        Returns:
            Callable: The wrapped function

        Examples:
            >>> execution_timer = ExecutionTimer()
            >>> @execution_timer.time_execution
            ... def my_func(a: int, b: int):
            ...     return a + b
            >>> for i in range(100):
            ...     my_func(i, i + 1)
            >>> execution_timer.get_execution_time(my_func)
            0.000123456789
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_time = time.perf_counter() - start_time
            self.times[name].append(elapsed_time)
            self.total_execution_times[name] += elapsed_time
            return result

        return wrapper

    def get_execution_times(self) -> Dict[str, float]:
        """Get the execution times of all functions that have been timed

        Returns:
            Dict[str, float]: A dictionary of function names to their execution times
        """
        return dict(self.total_execution_times)

    def get_execution_time(self, func: Union[Callable, str]) -> float:
        """Get the execution time of a specific function

        Args:
            func (Union[Callable, str]): The function to get the execution time for, as an instance of the function or the name of the function

        Returns:
            float: The execution time of the function
        """
        if isinstance(func, str):
            name = func
        else:
            name = func.__name__
        return self.total_execution_times[name]

    def pretty_print_times(self) -> None:
        """Print the execution times of all functions that have been timed"""
        avg_times = [
            self.total_execution_times[name] / len(self.times[name])
            for name in self.total_execution_times.keys()
        ]
        name_width = max(len(name) for name in self.total_execution_times.keys())
        time_width = max(
            len(f"{time:.6f}") for time in self.total_execution_times.values()
        )

        avg_time_width = max(len(f"{avg_time:.6f}") for avg_time in avg_times)

        name_width = max(name_width, len("Function"))
        time_width = max(time_width, len("Total Time (s)"))
        avg_time_width = max(avg_time_width, len("Average Time (s)"))

        print(
            f"{'Function':<{name_width}} | {'Total Time (s)':<{time_width}} | {'Average Time (s)':<{avg_time_width}}"
        )
        print("-" * (name_width + time_width + avg_time_width + 6))
        for idx, (name, total_time) in enumerate(self.total_execution_times.items()):
            avg_time = avg_times[idx]
            print(
                f"{name:<{name_width}} | {total_time:<{time_width}.6f} | {avg_time:<{avg_time_width}.6f}"
            )


class FunctionEvent:
    def __init__(
        self,
        function_name: str,
        start_time: float,
        end_time: float,
        function_arguments: Optional[Dict[str, Any]],
        function_returns: Optional[Any],
    ):
        self.name = function_name
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
        self.function_arguments = function_arguments
        self.function_returns = function_returns

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "function_arguments": self.function_arguments,
            "function_returns": self.function_returns,
        }

    def __repr__(self) -> str:
        return f"FunctionEvent(name={self.name}, start_time={self.start_time}, end_time={self.end_time}, duration={self.duration}, function_arguments={self.function_arguments}, function_returns={self.function_returns})"


class FunctionLogger:
    def __init__(self):
        self.logs: List[FunctionEvent] = []
        self.grouped_logs: Dict[str, List[FunctionEvent]] = defaultdict(list)
        self.idx = 0

    def log_function(self, log_args: bool = False, log_returns: bool = False):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                # Convert args and kwargs into single dict with same order as was passed
                if log_args:
                    argspec = inspect.getfullargspec(func)
                    arg_names = argspec.args
                    arg_dict = dict(zip(arg_names, args))
                    arg_dict.update(kwargs)
                    args = arg_dict

                event = FunctionEvent(
                    function_name=func.__name__,
                    start_time=start_time,
                    end_time=end_time,
                    function_arguments=args if log_args else None,
                    function_returns=result if log_returns else None,
                )
                self.logs.append(event)
                self.grouped_logs[func.__name__].append(event)
                return result

            return wrapper

        return decorator

    def get_logs(self) -> List[FunctionEvent]:
        """Get the logs of all functions that have been logged

        Returns:
            List[FunctionEvent]: A list of function logs
        """
        return self.logs

    def get_logs_by_function_name(
        self, function: Union[Callable, str]
    ) -> List[FunctionEvent]:
        """Get the logs of a specific function

        Args:
            function (Union[Callable, str]): The function to get the logs for, as an instance of the function or the name of the function

        Returns:
            List[FunctionEvent]: A list of function logs
        """
        if isinstance(function, str):
            name = function
        else:
            name = function.__name__
        return self.grouped_logs[name]

    def to_dict(self) -> List[Dict[str, Any]]:
        """Get the logs of all functions that have been logged as JSON

        Returns:
            List[Dict[str, Any]]: A list of function logs as JSON
        """
        return [log.to_dict() for log in self.logs]

    def write_jsonl(self, path: str) -> None:
        """Write the logs of all functions that have been logged to a JSONL file

        Args:
            path (str): The path to write the JSONL file to
        """
        with open(path, "w") as f:
            for log in self.logs:
                f.write(json.dumps(log.to_dict()) + "\n")

    def pretty_print_logs(self) -> None:
        """Prints the function name, start time, end time, and duration of all logs in a nice table"""
        name_width = max(len(log.name) for log in self.logs)
        time_width = max(len(f"{log.start_time:.6f}") for log in self.logs)
        duration_width = max(len(f"{log.duration:.6f}") for log in self.logs)

        name_width = max(name_width, len("Function"))
        time_width = max(time_width, len("Start Time (s)"))
        duration_width = max(duration_width, len("Duration (s)"))

        print(
            f"{'Function':<{name_width}} | {'Start Time (s)':<{time_width}} | {'Duration (s)':<{duration_width}}"
        )
        print("-" * (name_width + time_width + duration_width + 6))
        for log in self.logs:
            print(
                f"{log.name:<{name_width}} | {log.start_time:<{time_width}.6f} | {log.duration:<{duration_width}.6f}"
            )

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.logs):
            log = self.logs[self.idx]
            self.idx += 1
            return log
        else:
            raise StopIteration
