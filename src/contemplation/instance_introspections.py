import inspect
import gc
from collections import defaultdict
import time
from typing import (
    Dict,
    List,
    Callable,
    Union,
    Any,
    get_args,
    get_origin,
    Iterable,
    Generator,
)


def get_name_in_caller_scope(me: object):
    frame = (
        inspect.currentframe().f_back.f_back
    )  # Two steps back to get to the caller's scope
    local_vars = frame.f_locals
    names = [name for name, var in local_vars.items() if var is me]

    if names:
        return names[0]
    else:
        raise ValueError(f"Object not found in caller's local scope")


def get_name_in_all_scope(me: object):
    names = []
    frame = inspect.currentframe().f_back  # Start with the caller's frame

    while frame:
        local_vars = frame.f_locals
        names += [name for name, var in local_vars.items() if var is me]
        frame = frame.f_back  # Move to the previous frame

    return names


def how_many_of_type_exist(cls: type) -> int:
    return sum(isinstance(obj, cls) for obj in gc.get_objects())


def how_many_of_my_type_exist(me: object) -> int:
    return how_many_of_type_exist(type(me))


def what_are_my_names(cls: type) -> List[str]:
    return [name for name, obj in gc.get_objects() if isinstance(obj, cls)]


def where_am_i_from(me: object) -> str:
    return inspect.getsourcefile(me)
