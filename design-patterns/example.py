import time
import types
from functools import wraps
import celery


class Subscribe:
    def __init__(self, func):
        wraps(func)(self)
        self.is_subscribe = True

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


def timethis(func):
    '''
    Decorator that reports the execution time.
    '''

    # @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


@timethis
def countdown(n):
    '''
    Counts down
    '''
    while n > 0:
        n -= 1


@celery.task(queue='queue_name')
def add(a, b):
    return a + b
