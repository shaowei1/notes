from functools import partial


class HttpRequest(object):

    def __init__(self):
        self.method = "GET"
        self.body = b"name=abc@age=123"


class Foo(object):

    def __init__(self):
        self.request = HttpRequest()
        self.session = {"login":True,"is_super":False}

foo = Foo()

def func(args):
    return getattr(foo, args)

# 偏函数
re_func = partial(func,'request')
se_func = partial(func,'session')


class LocalProxy(object):

    def __init__(self,local):
        self._local = local

    def _get_current_object(self):
        return self._local()

    def __getitem__(self, item):
        return getattr(self._get_current_object(),item)

request = LocalProxy(re_func)
assert request._get_current_object().method == request['method'] == "GET"

session = LocalProxy(se_func)
assert session._get_current_object() == {"login":True,"is_super":False}