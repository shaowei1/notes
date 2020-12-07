"""
在多线程中，同一个进程中的多个线程是共享一个内存地址的，多个线程操作数据时，就会造成数据的不安全，所以我们就要加锁。
但是，对于一些变量，如果仅仅只在本线程中使用 threading.local

threading.local 在多线程操作时，为每一个线程创建一个值，使得线程之间各自操作自己的值，互不影响。
"""
import time
import threading
# from threading import current_thread as getcurrent
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
        # ident = threading.get_ident()
        ident = getcurrent()
        return self._storage[ident][item]

# local = threading.local()
local = Local()

def func(n):
    local.val = n
    time.sleep(2)
    print(local.val)

for i in range(10):
    t = threading.Thread(target=func,args=(i,))
    t.start()
