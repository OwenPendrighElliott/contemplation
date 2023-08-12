import inspect

from typing import Callable, Any, get_args, get_origin, Iterable, Generator


def _shallow_is_of_type(parameter: object, parameter_type: type) -> bool:
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


def strict_typing(func: Callable, deep: bool = True) -> Callable:
    type_checker = _deep_is_of_type if deep else _shallow_is_of_type
    signature = inspect.signature(func)
    parameters = signature.parameters
    return_annotation = signature.return_annotation
    return_type = return_annotation if return_annotation is not inspect._empty else None

    def wrapper(*args, **kwargs):
        for i, (name, parameter) in enumerate(parameters.items()):
            if parameter.annotation is inspect._empty:
                continue
            if i < len(args):
                if not type_checker(args[i], parameter.annotation):
                    raise TypeError(
                        f"Argument '{name}' for function '{func.__name__}' must be of type {parameter.annotation}, instead type {type(args[i])} was passed"
                    )
            elif name in kwargs:
                if not type_checker(kwargs[name], parameter.annotation):
                    raise TypeError(
                        f"Argument '{name}' for function '{func.__name__}' must be of type {parameter.annotation}, instead type {type(kwargs[name])} was passed"
                    )
        result = func(*args, **kwargs)

        if parameter.annotation is not inspect._empty and not type_checker(
            result, return_type
        ):
            raise TypeError(
                f"Return value for function '{func.__name__}' must be of type {return_type}, instead type {type(result)} was returned"
            )
        return result

    return wrapper