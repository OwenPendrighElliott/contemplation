# 🤔 Contemplation

Novel and powerful introspection utilities for Python.

Contemplation is a library for introspection of Python code. It provides a number of introspection utilities that are not available in the standard library. This library is designed to be used for debugging and analysing code.

```
pip install contemplation
```

## Introspections

There are three categories of introspection provided in this package:
+ Execution Introspections
+ Instance Introspections
+ Type Introspections
  
Exection introspections are introspections that are performed on the execution of code. Instance introspections are introspections that are performed on instances of objects. Type introspections are introspections that are performed on types. There are detailed below.

### Execution Introspections

The follow execution introspections are provided:
+ CallCounter - counts the number of times functions registered to it are called
+ ExecutionTimer - times the execution of functions registered to it
+ FunctionLogger - logs the times, arguments, and return values of functions registered to it

These class all act in very much the same way, they use function metadata to track the execution of functions. For example, you can time the execution of a function by wrapping it in an `ExecutionTimer` instance.

```python
import time
from contemplation import ExecutionTimer

execution_timer = ExecutionTimer()

@execution_timer.time_execution
def my_func(a: int, b: int):
    time.sleep(0.01)
    return a + b

for i in range(100):
    _ = my_func(i, i + 1)

# get the total execution time by function
print(execution_timer.get_execution_time(my_func))
# or by name
print(execution_timer.get_execution_time("my_func"))

# log another function
@execution_timer.time_execution
def my_other_func(a: int, b: int):
    time.sleep(0.005)
    return a - b

for i in range(100):
    _ = my_other_func(i, i + 1)

# print the times in a table
execution_timer.pretty_print_times()
```

The same API applies to the `CallCounter`:

```python
import time
from contemplation import CallCounter

call_counter = CallCounter()

@call_counter.count_calls
def my_func(a: int, b: int):
    return a + b

for i in range(100):
    _ = my_func(i, i + 1)

# get the total execution time by function
print(call_counter.get_counts(my_func))
# or by name
print(call_counter.get_counts("my_func"))

# log another function
@call_counter.count_calls
def my_other_func(a: int, b: int):
    return a - b

for i in range(50):
   _ = my_other_func(i, i + 1)

# print the times in a table
call_counter.pretty_print_counts()
```

The `FunctionLogger` is a little different, it logs the arguments and return values of functions. It can be used to log the execution of functions to a file. The decorator for function logger has arguments as well.

```python
from contemplation import FunctionLogger

function_logger = FunctionLogger()

@function_logger.log_function(log_args=True, log_returns=True)
def my_func(a: int, b: int):
    return a + b

_ = my_func(1, 2)

function_logger.pretty_print_logs()

# log another function
@function_logger.log_function(log_args=True, log_returns=True)
def my_other_func(a: int, b: int):
    return a - b

_ = my_other_func(3, 4)
_ = my_func(5, 6)

for event in function_logger:
    print(event)

```

### Instance Introspections

Instance introspections are introspections that are performed on instances of objects. The following instance introspections are provided, they are poised as questions:
+ how_many_of_my_type_exist - how many instances of a type exist given an instance
+ how_many_of_type_exist - how many instances of a type exist given a type
+ get_name_in_caller_scope - get the name an instance was assigned to in the scope of the caller
+ get_name_in_all_scope - get the name an instance was assigned to in the scope of the caller and all parent scopes

These introspections are useful for debugging and analysing code. For example, you can use `how_many_of_my_type_exist` and `how_many_of_type_exist` to find out how many instances of a type exist given an instance.

```python
from contemplation import how_many_of_my_type_exist, how_many_of_type_exist

class MyClass:
    pass

my_instance = MyClass()
my_instance_2 = MyClass()

print(how_many_of_my_type_exist(my_instance))

print(how_many_of_type_exist(MyClass))
```

You can use `get_name_in_caller_scope` an instance was assigned to in the scope of the caller.

```python
from contemplation import get_name_in_caller_scope, get_name_in_all_scope

class MyClass:
    pass

my_class = MyClass()

def my_func1(obj: object):
    print(get_name_in_caller_scope(obj))
    assert get_name_in_caller_scope(obj) == "my_class"

my_func1(my_class)

dd = defaultdict(int)

def my_func2(obj: object):
    print(get_name_in_caller_scope(obj))
    assert get_name_in_caller_scope(obj) == "dd"

my_func2(dd)
```

You can use `get_name_in_all_scope` an instance was assigned to in the scope of the caller and all parent scopes. This is very powerful for tracing how a variable made its way somewhere but can also be a bit confusing.

```python
 def f1(a):
    print(get_name_in_all_scope(a))
    return get_name_in_all_scope(a)

def f2(b):
    return f1(b)

def f3(c):
    return f2(c)

def f4(d):
    return f3(d)

names = f4(1)
assert names[3] == "d"
assert names[2] == "c"
assert names[1] == "b"
assert names[0] == "a"
```

### Type Introspections

Type introspections are introspections that are performed on types. Currently there the `@type_enforced()` decorator and the `introspect_type` function. 

You can use `introspect_type` to get the actual type of an object. This will recurse through the object and build a type annotation.

```python
from contemplation import introspect_type

d = {"a": [1, 2, 3], "b": [4, 5, 6]}
print(introspect_type(d))

d = {"a": [1, 2, 3], "b": [4, 5, "6"]}
print(introspect_type(d))
```


The `@type_enforced()` decorator can be used to enforce the type of a function's arguments and return value.

This uses the annotations on the functions to check the types of the arguments against what was received. 

You can toggle between shallow and deep type checking. Shallow will not work with annotations from the `typing` module however deep will. Deep is the default.

__Don't use this outside of debugging, deep type checking will check every element of every iterable at every depth every time the function is called. This is slow.__

```python
from typing import Dict, List
from contemplation import type_enforced

@type_enforced(deep=True)
def test_func(d: Dict[str, List[int]]) -> int:
    s = 0
    for k in d:
        s += sum(d[k])
    return s

# this works no problems
d = {"a": [1, 2, 3], "b": [4, 5, 6]}
print(test_func(d))

# this fails
d = {"a": [1, 2, 3], "b": [4, 5, "6"]}
print(test_func(d))
```

A failed type check will print a detailed specification of the type that was received.

```
TypeError: Argument 'd' for function 'test_func' must be of type typing.Dict[str, typing.List[int]], instead type typing.Dict[str, typing.Union[typing.List[typing.Union[int, str]], typing.List[int]]] was passed
```

You can also get this type information directly for any object:

```python
from contemplation import introspect_type

my_dict = {"a": [1, 2, 3], "b": [4, 5, 6]}

print(introspect_type(my_dict))
```

This will print `typing.Dict[str, typing.List[int]]`.

The type introspection occurs recursively for arbitrarily complex objects.

# Documentation

Documentation is located at `docs/index.html`.

You can generate documentation with `pdoc3`.

```
pip3 install pdoc3
```

```
pdoc3 --html --output-dir docs contemplation --force
```