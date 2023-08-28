import pytest
import typing
from typing import List, Dict, Union
from contemplation import _shallow_is_of_type, _deep_is_of_type, type_enforced


def test_native_shallow_is_of_type_int():
    a = 1
    assert _shallow_is_of_type(a, int)
    assert not _shallow_is_of_type(a, float)
    assert not _shallow_is_of_type(a, str)


def test_native_shallow_is_of_type_list():
    x = [1, 2, 3]
    assert _shallow_is_of_type(x, list)
    assert not _shallow_is_of_type(x, tuple)
    assert not _shallow_is_of_type(x, dict)
    assert not _shallow_is_of_type(x, set)
    assert not _shallow_is_of_type(x, str)


def test_native_shallow_is_of_type_tuple():
    y = (1, 2, 3)
    assert _shallow_is_of_type(y, tuple)
    assert not _shallow_is_of_type(y, list)
    assert not _shallow_is_of_type(y, dict)
    assert not _shallow_is_of_type(y, set)
    assert not _shallow_is_of_type(y, str)


def test_native_shallow_is_of_type_dict():
    z = {"a": 1, "b": 2}
    assert _shallow_is_of_type(z, dict)
    assert not _shallow_is_of_type(z, list)
    assert not _shallow_is_of_type(z, tuple)
    assert not _shallow_is_of_type(z, set)
    assert not _shallow_is_of_type(z, str)


def test_native_shallow_is_of_type_set():
    s = {1, 2, 3}
    assert _shallow_is_of_type(s, set)
    assert not _shallow_is_of_type(s, list)
    assert not _shallow_is_of_type(s, tuple)
    assert not _shallow_is_of_type(s, dict)
    assert not _shallow_is_of_type(s, str)


def test_native_shallow_is_of_type_str():
    t = "hello"
    assert _shallow_is_of_type(t, str)
    assert not _shallow_is_of_type(t, list)
    assert not _shallow_is_of_type(t, tuple)
    assert not _shallow_is_of_type(t, dict)
    assert not _shallow_is_of_type(t, set)
    assert not _shallow_is_of_type(t, int)
    assert not _shallow_is_of_type(t, float)


def test_native_shallow_is_of_type_float():
    f = 1.2
    assert _shallow_is_of_type(f, float)
    assert not _shallow_is_of_type(f, list)
    assert not _shallow_is_of_type(f, tuple)
    assert not _shallow_is_of_type(f, dict)
    assert not _shallow_is_of_type(f, set)
    assert not _shallow_is_of_type(f, int)
    assert not _shallow_is_of_type(f, str)


def test_typing_shallow_is_of_type_int():
    x = [1, 2, 3]
    assert _shallow_is_of_type(x, typing.List)
    assert _shallow_is_of_type(x, typing.Any)
    assert _shallow_is_of_type(x, typing.Iterable)
    assert not _shallow_is_of_type(x, typing.Tuple)
    assert not _shallow_is_of_type(x, typing.Dict)
    assert not _shallow_is_of_type(x, typing.Set)
    assert not _shallow_is_of_type(x, typing.Callable)


def test_typing_shallow_is_of_type_tuple():
    y = (1, 2, 3)
    assert _shallow_is_of_type(y, typing.Tuple)
    assert _shallow_is_of_type(y, typing.Any)
    assert _shallow_is_of_type(y, typing.Iterable)
    assert not _shallow_is_of_type(y, typing.List)
    assert not _shallow_is_of_type(y, typing.Dict)
    assert not _shallow_is_of_type(y, typing.Set)
    assert not _shallow_is_of_type(y, typing.Callable)


def test_typing_shallow_is_of_type_dict():
    z = {"a": 1, "b": 2}
    assert _shallow_is_of_type(z, typing.Dict)
    assert _shallow_is_of_type(z, typing.Any)
    assert _shallow_is_of_type(z, typing.Mapping)
    assert not _shallow_is_of_type(z, typing.List)
    assert not _shallow_is_of_type(z, typing.Tuple)
    assert not _shallow_is_of_type(z, typing.Set)
    assert not _shallow_is_of_type(z, typing.Callable)


def test_typing_shallow_is_of_type_set():
    s = {1, 2, 3}
    assert _shallow_is_of_type(s, typing.Set)
    assert _shallow_is_of_type(s, typing.Any)
    assert _shallow_is_of_type(s, typing.Iterable)
    assert not _shallow_is_of_type(s, typing.List)
    assert not _shallow_is_of_type(s, typing.Tuple)
    assert not _shallow_is_of_type(s, typing.Dict)
    assert not _shallow_is_of_type(s, typing.Callable)


def test_typing_shallow_is_of_type_str():
    t = "hello"
    assert _shallow_is_of_type(t, typing.Any)
    assert _shallow_is_of_type(t, typing.Iterable)
    assert _shallow_is_of_type(t, typing.Sized)
    assert _shallow_is_of_type(t, typing.Sequence)
    assert not _shallow_is_of_type(t, typing.List)
    assert not _shallow_is_of_type(t, typing.Tuple)
    assert not _shallow_is_of_type(t, typing.Dict)
    assert not _shallow_is_of_type(t, typing.Set)
    assert not _shallow_is_of_type(t, typing.Callable)
    assert not _shallow_is_of_type(t, typing.Mapping)
    assert not _shallow_is_of_type(t, typing.MutableSequence)
    assert not _shallow_is_of_type(t, typing.MutableMapping)
    assert not _shallow_is_of_type(t, typing.ByteString)
    assert not _shallow_is_of_type(t, typing.MutableSet)
    assert not _shallow_is_of_type(t, typing.MutableMapping)
    assert not _shallow_is_of_type(t, typing.ByteString)
    assert not _shallow_is_of_type(t, typing.MutableSet)
    assert not _shallow_is_of_type(t, typing.MappingView)


def test_typing_shallow_is_of_type_callable():
    def test_func():
        ...

    assert _shallow_is_of_type(test_func, typing.Callable)


def test_typing_shallow_is_of_type_list():
    x = [1, 2, 3]
    assert _shallow_is_of_type(x, typing.Union[typing.List, typing.Tuple])


def test_typing_shallow_is_of_type_tuple():
    xt = (1, 2, 3)
    assert _shallow_is_of_type(xt, typing.Union[typing.List, typing.Tuple])


def test_native_deep_is_of_type_int():
    a = 1
    assert _deep_is_of_type(a, int)
    assert not _deep_is_of_type(a, float)
    assert not _deep_is_of_type(a, str)


def test_native_deep_is_of_type_list():
    x = [1, 2, 3]
    assert _deep_is_of_type(x, list)
    assert not _deep_is_of_type(x, tuple)
    assert not _deep_is_of_type(x, dict)
    assert not _deep_is_of_type(x, set)
    assert not _deep_is_of_type(x, str)


def test_native_deep_is_of_type_tuple():
    y = (1, 2, 3)
    assert _deep_is_of_type(y, tuple)
    assert not _deep_is_of_type(y, list)
    assert not _deep_is_of_type(y, dict)
    assert not _deep_is_of_type(y, set)
    assert not _deep_is_of_type(y, str)


def test_native_deep_is_of_type_dict():
    z = {"a": 1, "b": 2}
    assert _deep_is_of_type(z, dict)
    assert not _deep_is_of_type(z, list)
    assert not _deep_is_of_type(z, tuple)
    assert not _deep_is_of_type(z, set)
    assert not _deep_is_of_type(z, str)


def test_native_deep_is_of_type_set():
    s = {1, 2, 3}
    assert _deep_is_of_type(s, set)
    assert not _deep_is_of_type(s, list)
    assert not _deep_is_of_type(s, tuple)
    assert not _deep_is_of_type(s, dict)
    assert not _deep_is_of_type(s, str)


def test_native_deep_is_of_type_str():
    t = "hello"
    assert _deep_is_of_type(t, str)
    assert not _deep_is_of_type(t, list)
    assert not _deep_is_of_type(t, tuple)
    assert not _deep_is_of_type(t, dict)
    assert not _deep_is_of_type(t, set)
    assert not _deep_is_of_type(t, int)
    assert not _deep_is_of_type(t, float)


def test_native_deep_is_of_type_float():
    f = 1.2
    assert _deep_is_of_type(f, float)
    assert not _deep_is_of_type(f, list)
    assert not _deep_is_of_type(f, tuple)
    assert not _deep_is_of_type(f, dict)
    assert not _deep_is_of_type(f, set)
    assert not _deep_is_of_type(f, int)
    assert not _deep_is_of_type(f, str)


def test_typing_deep_is_of_type_list():
    x = [1, 2, 3]
    assert _deep_is_of_type(x, typing.List[int])
    assert not _deep_is_of_type(x, typing.List[float])
    assert _deep_is_of_type(x, typing.Any)
    assert not _deep_is_of_type(x, typing.Tuple)
    assert not _deep_is_of_type(x, typing.Dict)
    assert not _deep_is_of_type(x, typing.Set)
    assert not _deep_is_of_type(x, typing.Callable)


def test_typing_deep_is_of_type_tuple():
    y = (1, 2, 3)
    assert _deep_is_of_type(y, typing.Tuple[int])
    assert not _deep_is_of_type(y, typing.Tuple[str])
    assert _deep_is_of_type(y, typing.Any)
    assert not _deep_is_of_type(y, typing.List)
    assert not _deep_is_of_type(y, typing.Dict)
    assert not _deep_is_of_type(y, typing.Set)
    assert not _deep_is_of_type(y, typing.Union)
    assert not _deep_is_of_type(y, typing.Callable)


def test_typing_deep_is_of_type_dict():
    z = {"a": 1, "b": 2}
    assert _deep_is_of_type(z, typing.Dict[str, int])
    assert _deep_is_of_type(z, typing.Any)
    assert not _deep_is_of_type(z, typing.List)
    assert _deep_is_of_type(z, typing.Dict)


def test_typing_deep_is_of_type_set():
    s = {"1", "2", "3"}
    assert _deep_is_of_type(s, typing.Set)
    assert _deep_is_of_type(s, typing.Set[str])
    assert not _deep_is_of_type(s, typing.Set[int])
    assert _deep_is_of_type(s, typing.Any)


def test_typing_deep_is_of_type_str():
    t = "hello"
    assert _deep_is_of_type(t, typing.Any)


def test_typing_deep_is_of_type_callable():
    def test_func():
        ...

    assert _deep_is_of_type(test_func, typing.Callable)


def test_type_checking_shallow():
    @type_enforced(deep=False)
    def test_func(a: int, b: str) -> str:
        return str(a + int(b))

    try:
        test_func(1, "2")
        assert True
    except TypeError:
        pytest.fail("Type checking failed unexpectedly for valid input")

    @type_enforced(deep=False)
    def test_func(a: int, b: int) -> str:
        return str(a + int(b))

    try:
        test_func(1, "2")
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True

    @type_enforced(deep=False)
    def test_func(a: int, b: str) -> int:
        return str(a + int(b))

    try:
        test_func(1, "2")
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True


def test_type_checking_shallow_typing():
    @type_enforced(deep=False)
    def test_func(a: list) -> int:
        return int(a[0])

    try:
        test_func([1, 2, 3])
        assert True
    except TypeError:
        pytest.fail("Type checking failed unexpectedly for valid input")

    try:
        test_func(2)
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True

    try:
        test_func([1, 2, "3"])
        assert True
    except TypeError:
        pytest.fail("Type checking failed unexpectedly for valid input")


def test_type_checking_deep():
    @type_enforced()
    def test_func(a: int, b: str) -> str:
        return str(a + int(b))

    try:
        test_func(1, "2")
        assert True
    except TypeError:
        pytest.fail("Type checking failed unexpectedly for valid input")

    @type_enforced()
    def test_func(a: int, b: int) -> str:
        return str(a + int(b))

    try:
        test_func(1, "2")
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True

    @type_enforced()
    def test_func(a: int, b: str) -> int:
        return str(a + int(b))

    try:
        test_func(1, "2")
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True


def test_type_checking_deep_typing():
    @type_enforced()
    def test_func(a: List[int]) -> int:
        return sum(a)

    try:
        test_func([1, 2, 3])
        assert True
    except TypeError:
        pytest.fail("Type checking failed unexpectedly for valid input")

    try:
        test_func(2)
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True

    try:
        test_func([1, 2, "3"])
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True

    @type_enforced()
    def test_func(a: Dict[str, List[int]]) -> Dict[str, List[int]]:
        return a

    try:
        test_func({"a": [1, 2, 3]})
        assert True
    except TypeError:
        pytest.fail("Type checking failed unexpectedly for valid input")

    try:
        test_func({"a": [1, 2, "3"]})
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True

    try:
        test_func({"a": [1, "2", 3], "b": [1, 2, "3"]})
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True

    try:
        test_func({"a": [1, 2, 3], "b": [1, 2, 3]})
        assert True
    except TypeError:
        pytest.fail("Type checking failed unexpectedly for valid input")

    @type_enforced()
    def test_func_2(a: Dict[str, List[Union[str, int]]]) -> int:
        return 5

    try:
        test_func_2({"a": [1, "2", 3], "b": [1, 2, "3"]})
        assert True
    except TypeError:
        pytest.fail("Type checking passed unexpectedly for invalid input")

    try:
        test_func_2({"a": [1, "2", [3, 2]], "b": [1, 2, "3"]})
        pytest.fail("Type checking passed unexpectedly for invalid input")
    except TypeError:
        assert True
