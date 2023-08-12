from collections import defaultdict
import time
from functools import wraps
from typing import Dict, Callable, Union


class CallCounter:
    def __init__(self):
        self.counts: Dict[str, int] = defaultdict(int)

    def count_calls(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            self.counts[name] += 1
            return func(*args, **kwargs)

        return wrapper

    def get_counts(self) -> Dict[str, int]:
        return dict(self.counts)

    def get_count(self, func: Union[Callable, str]) -> int:
        if isinstance(func, str):
            name = func
        else:
            name = func.__name__
        return self.counts[name]

    def pretty_print_counts(self) -> None:
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
        return dict(self.total_execution_times)

    def get_execution_time(self, func: Union[Callable, str]) -> float:
        if isinstance(func, str):
            name = func
        else:
            name = func.__name__
        return self.total_execution_times[name]

    def pretty_print_times(self) -> None:
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
        print("-" * (name_width + time_width + 3))
        for idx, (name, total_time) in enumerate(self.total_execution_times.items()):
            avg_time = avg_times[idx]
            print(
                f"{name:<{name_width}} | {total_time:<{time_width}.6f} | {total_time:<{avg_time_width}.6f}"
            )
