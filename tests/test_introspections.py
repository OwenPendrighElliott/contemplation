from collections import defaultdict
from contemplation import (
    how_many_of_my_type_exist,
    how_many_of_type_exist,
    get_name_in_caller_scope,
    get_name_in_all_scope,
)


def test_get_name_in_caller_scope():
    class MyClass:
        pass

    my_class = MyClass()

    def my_func1(obj: object):
        assert get_name_in_caller_scope(obj) == "my_class"

    my_func1(my_class)

    dd = defaultdict(int)

    def my_func2(obj: object):
        assert get_name_in_caller_scope(obj) == "dd"

    my_func2(dd)


def test_how_many_of_type_exist():
    class MyClass:
        pass

    my_class = MyClass()

    assert how_many_of_type_exist(MyClass) == 1

    my_class_v2 = MyClass()

    assert how_many_of_type_exist(MyClass) == 2

    assert how_many_of_my_type_exist(my_class) == 2
    assert how_many_of_my_type_exist(my_class_v2) == 2
