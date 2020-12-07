from greenlet import getcurrent

class Local(object):

    def __init__(self):
        object.__setattr__(self, "_storage", {})

    def __setattr__(self, key, value):

        # ident = threading.get_ident()
        ident = getcurrent()   # 定制粒度更细的
        if ident in self._storage:
            self._storage[ident][key] = value
        else:
            self._storage[ident] = {key:value}

    def __getattr__(self, item):
        # 反射机制
        # ident = threading.get_ident()
        ident = getcurrent()
        return self._storage[ident][item]


class LocalStack(object):

    def __init__(self):
        self.local = Local()

    def push(self, item):
        self.local.stack = []
        self.local.stack.append(item)

    def pop(self):
        return self.local.stack.pop()

    def top(self):
        return self.local.stack[-1]

_local_stack = LocalStack()
_local_stack.push(55)
print(_local_stack.top())  # 取栈顶元素

# 利用栈