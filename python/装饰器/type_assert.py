"""
强制类型检查
https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p07_enforcing_type_check_on_function_using_decorator.html
"""
from inspect import signature
from functools import wraps
# typeguard-2.9.1
from typeguard import check_type
# typing-inspect-0.6.0
from typing_inspect import get_parameters
from typing_inspect import get_origin

import typing


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    try:
                        # Checking if a variable conforms to a typing object
                        check_type('assert type', value, bound_types[name])
                    except TypeError as e:
                        raise e
            return func(*args, **kwargs)

        return wrapper

    return decorate


def typeassert_origin(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
            return func(*args, **kwargs)

        return wrapper

    return decorate


@typeassert(int, typing.List[int])
def add(x, y):
    assert check_type('type', [2], typing.List[int]) is None
    assert typing.List[str].__origin__ == list
    assert get_origin(typing.List[str]) == list
    assert typing.List[str].__args__[0] == str
    # assert get_parameters(typing.List[str])[0] == str
    return f'{x} + {y}'


add(2, [2, 1])


# add(2, 'hello')


@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)


spam(1, 2, 3)
spam(1, 'hello', 3)


# spam(1, 'hello', 'world')

@typeassert(int, list)
def bar(x, items=None):
    """
    它对于有默认值的参数并不适用。 比如下面的代码可以正常工作，尽管items的类型是错误的：
    :param x:
    :param items:
    :return:
    """
    if items is None:
        items = []
    items.append(x)
    return items


bar(2)
bar(4, [1, 2, 3])
# bar(2, 3)
