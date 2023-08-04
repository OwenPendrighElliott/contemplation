import inspect
import gc
from collections import defaultdict
from typing import Dict, Callable, Union

def what_is_my_name(me: object) -> str:
    for ref in gc.get_referrers(me):
        if type(ref) is dict:
            for k, v in ref.items():
                if v is me:
                    return k
    raise ValueError("I could not find myself in globals()")

def what_is_my_code(me: object) -> str:
    return inspect.getsource(me)

def how_many_of_type_exist(cls: type) -> int:
    return sum(isinstance(val, cls) for val in globals().values())

def how_many_of_me_exist(me: object) -> int:
    cls = type(me)
    return how_many_of_type_exist(cls)

class CallCounter:
    def __init__(self):
        self.counts: Dict[str, int] = defaultdict(int)

    def count_calls(self, func: Callable) -> Callable:
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
        print('-' * (name_width + count_width + 3))
        for name, count in self.counts.items():
            print(f"{name:<{name_width}} | {count:<{count_width}}")
