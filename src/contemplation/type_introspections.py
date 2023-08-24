import inspect

from typing import (
    Callable,
    Any,
    get_args,
    get_origin,
    Iterable,
    Generator,
    Union,
    Dict,
    List,
)


def _make_union(types: List[type]):
    return Union[tuple(types)]


def introspect_type(obj: Any) -> Any:
    if isinstance(obj, dict):
        key_types = {introspect_type(key) for key in obj.keys()}
        value_types = {introspect_type(value) for value in obj.values()}
        key_type = key_types.pop() if len(key_types) == 1 else _make_union(key_types)
        value_type = (
            value_types.pop() if len(value_types) == 1 else _make_union(value_types)
        )
        return Dict[key_type, value_type]
    elif isinstance(obj, list):
        element_types = {introspect_type(element) for element in obj}
        element_type = (
            element_types.pop()
            if len(element_types) == 1
            else _make_union(element_types)
        )
        return List[element_type]

    return type(obj)


def _shallow_is_of_type(parameter: object, parameter_type: type) -> bool:
    """Check if an object is of a given type, without checking the types of its members

    Args:
        parameter (object): The parameter to check the type of
        parameter_type (type): The type that is annotated for the parameter

    Returns:
        bool: Whether the parameter is of the given type
    """
    if parameter_type is Any:
        return True

    origin = get_origin(parameter_type)
    if origin is None:
        return isinstance(parameter, parameter_type)

    if origin in {list, tuple, set, frozenset, dict, Iterable, Generator}:
        args = get_args(parameter_type)
        if not args:
            return isinstance(parameter, origin)
        if origin is dict:
            key_type, value_type = args
            return all(
                _shallow_is_of_type(k, key_type) and _shallow_is_of_type(v, value_type)
                for k, v in parameter.items()
            )
        elif origin is Generator:
            if not hasattr(parameter, "next") and not hasattr(parameter, "__next__"):
                return False
            return True
        elif origin is Iterable:
            (element_type,) = args
            return all(_shallow_is_of_type(item, element_type) for item in parameter)
        else:
            (element_type,) = args
            return all(_shallow_is_of_type(item, element_type) for item in parameter)
    elif origin is Callable:
        if not hasattr(parameter, "__call__"):
            return False
        return True
    return isinstance(parameter, parameter_type)


def _deep_is_of_type(parameter: object, parameter_type: type) -> bool:
    """Check if an object is of a given type, checking the types of its members

    Args:
        parameter (object): The parameter to check the type of
        parameter_type (type): The type that is annotated for the parameter

    Returns:
        bool: Whether the parameter is of the given type
    """
    from typing import Union

    if parameter_type is Any:
        return True

    if isinstance(parameter_type, type(Union)):
        return any(_deep_is_of_type(parameter, t) for t in get_args(parameter_type))

    origin = get_origin(parameter_type)
    if origin is None:
        return isinstance(parameter, parameter_type)

    args = get_args(parameter_type)

    if args:
        if origin is dict:
            key_type, value_type = args
            return all(
                _deep_is_of_type(k, key_type) and _deep_is_of_type(v, value_type)
                for k, v in parameter.items()
            )
        elif origin is Generator:
            if not hasattr(parameter, "next") and not hasattr(parameter, "__next__"):
                return False
            return True
        elif origin is Callable:
            if not hasattr(parameter, "__call__"):
                return False
            return True
        elif origin in {list, tuple, set, frozenset}:
            (element_type,) = args
            return all(_deep_is_of_type(item, element_type) for item in parameter)
        elif origin is Iterable:
            return (
                all(
                    _deep_is_of_type(item, get_args(parameter_type)[0])
                    for item in parameter
                )
                if isinstance(parameter, Iterable)
                else False
            )

    return isinstance(parameter, parameter_type)


def type_enforced(deep: bool = True):
    def decorator(func: Callable) -> Callable:
        """Decorator that enforces the types of the arguments and return value of a function

        Args:
            deep (bool, optional): Whether or not the type checking should look at members of the type. Defaults to True.

        Raises:
            TypeError: An argument or return value does not match the annotations on the function
        Returns:
            Callable: The function to enforce type checking on

        Examples:
            >>> @type_enforced
            ... def test_func(a: int, b: str) -> str:
            ...     return str(a + int(b))
            ...
            >>> test_func(1, "2")
            "3"
            >>> test_func(1, 2)
            TypeError: Argument 'b' for function 'test_func' must be of type <class 'str'>, instead type <class 'int'> was passed
            >>> test_func(1, "2.0")
            TypeError: Return value for function 'test_func' must be of type <class 'str'>, instead type <class 'float'> was returned
        """

        type_checker = _deep_is_of_type if deep else _shallow_is_of_type
        signature = inspect.signature(func)
        parameters = signature.parameters
        return_annotation = signature.return_annotation
        return_type = (
            return_annotation if return_annotation is not inspect._empty else None
        )

        def wrapper(*args, **kwargs):
            for i, (name, parameter) in enumerate(parameters.items()):
                if parameter.annotation is inspect._empty:
                    continue
                if i < len(args):
                    if not type_checker(args[i], parameter.annotation):
                        raise TypeError(
                            f"Argument '{name}' for function '{func.__name__}' must be of type {parameter.annotation}, instead type {introspect_type(args[i])} was passed"
                        )
                elif name in kwargs:
                    if not type_checker(kwargs[name], parameter.annotation):
                        raise TypeError(
                            f"Argument '{name}' for function '{func.__name__}' must be of type {parameter.annotation}, instead type {introspect_type(kwargs[name])} was passed"
                        )
            result = func(*args, **kwargs)

            if parameter.annotation is not inspect._empty and not type_checker(
                result, return_type
            ):
                raise TypeError(
                    f"Return value for function '{func.__name__}' must be of type {return_type}, instead type {introspect_type(result)} was returned"
                )
            return result

        return wrapper

    return decorator
