import inspect
import gc
from typing import List


def get_name_in_caller_scope(me: object) -> str:
    """Get the name of an object in the caller's local scope

    Args:
        me (object): The object to get the name of

    Raises:
        ValueError: If the object is not found in the caller's local scope

    Returns:
        str: The name of the object in the caller's local scope
    """
    frame = (
        inspect.currentframe().f_back.f_back
    )  # Two steps back to get to the caller's scope
    local_vars = frame.f_locals
    names = [name for name, var in local_vars.items() if var is me]

    if names:
        return names[0]
    else:
        raise ValueError(f"Object not found in caller's local scope")


def get_name_in_all_scope(me: object) -> List[str]:
    """Get the name of an object in all parent scopes

    Args:
        me (object): The object to get the names of

    Returns:
        List[str]: The names of the object in all parent scopes
    """
    names = []
    frame = inspect.currentframe().f_back  # Start with the caller's frame

    while frame:
        local_vars = frame.f_locals
        names += [name for name, var in local_vars.items() if var is me]
        frame = frame.f_back  # Move to the previous frame

    return names


def how_many_of_type_exist(cls: type) -> int:
    """Count how many objects of a given type exist

    Args:
        cls (type): The type to count

    Returns:
        int: The number of objects of the given type that exist
    """
    return sum(isinstance(obj, cls) for obj in gc.get_objects())


def how_many_of_my_type_exist(me: object) -> int:
    """Count how many objects of the same type as me exist

    Args:
        me (object): The object to count the type of

    Returns:
        int: The number of objects of the same type as me that exist
    """
    return how_many_of_type_exist(type(me))
