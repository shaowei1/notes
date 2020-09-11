### 线程安全的操作
> A global interpreter lock (GIL) is used internally to ensure that only one thread runs in the Python VM at a time. In general, Python offers to switch among threads only between bytecode instructions; how frequently it switches can be set via sys.setswitchinterval(). 
>
> https://docs.python.org/3.5/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe
- There are

```
L.append(x)
L1.extend(L2)
x = L[i]
x = L.pop()
L1[i:j] = L2
L.sort()
x = y
x.field = y
D[x] = y
D1.update(D2)
D.keys()
```

- These aren’t:
```
i = i+1
L.append(L[-1])
L[i] = L[j]
D[x] = D[x] + 1
```
#### dis
> 每一行表示执行这个fun函数的过程，可以被拆分成这些步骤，导入全局变量-->导入常数-->执行加法-->存储变量……，这里每一个步骤都是指令字节码，可以看做原子操作

```python
from dis import dis

a = 0


def fun():
    global a
    a = a + 1


dis(fun)
"""
a = a + 1这个过程包含了几个指令，可以看到它包含了两个，即BINARY_ADD和STORE_GLOBAL，
如果在前者(运算加和)执行后，后者(赋值)还没开始时，切换了线程，就会出现修改资源冲突。

  8           0 LOAD_GLOBAL              0 (a)
              2 LOAD_CONST               1 (1)
              4 BINARY_ADD
              6 STORE_GLOBAL             0 (a)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE

"""
```

```python
from dis import dis

l = []


def fun():
    global l
    l.append(1)


dis(fun)
"""
append其实只有POP_TOP这一步，要么执行，要么不执行，不会出现被中断的问题
 20           0 LOAD_GLOBAL              0 (l)
              2 LOAD_METHOD              1 (append)
              4 LOAD_CONST               1 (1)
              6 CALL_METHOD              1
              8 POP_TOP
             10 LOAD_CONST               0 (None)
             12 RETURN_VALUE
"""
```

#### 线程不安全
```python
import threading
zero = 0
def change_zero():
    global zero
    for i in range(3000000):
        zero += 1
        zero -= 1

th1 = threading.Thread(target = change_zero)
th2 = threading.Thread(target = change_zero)
th1.start()
th2.start()
th1.join()
th2.join()
print(zero)

```
#### 人工原子操作(atomic operation) ==> 线程安全
```python
import threading

shared_resource_lock = threading.Lock()
zero = 0


class Lock:
    def __init__(self, tag=None):
        self.tag = tag

    def __enter__(self):
        shared_resource_lock.acquire()
        return self  # 可以返回不同的对象

    def __exit__(self, exc_type, exc_value, exc_tb):
        """

        :param self:
        :param exc_type：　错误的类型
        :param exc_value：　错误类型对应的值
        :param exc_tb：　代码中错误发生的位置
        :return:
        """
        shared_resource_lock.release()
        # 如果 __exit__ 返回 True，则异常被忽略；如果返回 False，则重新抛出异常
        return False  # 可以省略，缺省的None也是被看做是False


def change_zero():
    global zero
    for i in range(1000000):
        with Lock():
            zero += 1
            zero -= 1


th1 = threading.Thread(target=change_zero)
th2 = threading.Thread(target=change_zero)
th1.start()
th2.start()
th1.join()
th2.join()
print(zero)
```

### WITH执行流程
```markdown
context_manager = context_expression
    exit = type(context_manager).__exit__
    value = type(context_manager).__enter__(context_manager)
    exc = True   # True 表示正常执行，即便有异常也忽略；False 表示重新抛出异常，需要对异常进行处理
    try:
        try:
            target = value  # 如果使用了 as 子句
            with-body     # 执行 with-body
        except:
            # 执行过程中有异常发生
            exc = False
            # 如果 __exit__ 返回 True，则异常被忽略；如果返回 False，则重新抛出异常
            # 由外层代码对异常进行处理
            if not exit(context_manager, *sys.exc_info()):
                raise
    finally:
        # 正常退出，或者通过 statement-body 中的 break/continue/return 语句退出
        # 或者忽略异常退出
        if exc:
            exit(context_manager, None, None, None)
        # 缺省返回 None，None 在布尔上下文中看做是 False
```

### LOCK WITH CONDITION
> 维护一个整数列表integer_list，共有两个线程
>
> Producer类对应一个线程，功能：随机产生一个整数，加入整数列表之中
>
> Consumer类对应一个线程，功能：从整数列表中pop掉一个整数
>
> 通过time.sleep来表示两个线程运行速度，设置成Producer产生的速度没有Consumer消耗的快

```python
# lock
import time
import threading
import random


class Producer(threading.Thread):

    # 产生随机数，将其加入整数列表
    def __init__(self, lock, integer_list):
        threading.Thread.__init__(self)
        self.lock = lock
        self.integer_list = integer_list

    def run(self):
        while True:  # 一直尝试获得锁来添加整数
            random_integer = random.randint(0, 100)
            with self.lock:
                self.integer_list.append(random_integer)
                print(f'integer list add integer {random_integer}')
            time.sleep(1.2 * random.random())  # sleep随机时间，通过乘1.2来减慢生产的速度


class Consumer(threading.Thread):

    def __init__(self, lock, integer_list):
        threading.Thread.__init__(self)
        self.lock = lock
        self.integer_list = integer_list

    def run(self):
        while True:  # 一直尝试去消耗整数
            with self.lock:
                if self.integer_list:  # 只有列表中有元素才pop
                    integer = self.integer_list.pop()
                    print(f'integer list lose integer {integer}')
                    time.sleep(random.random())
                else:
                    print('there is no integer in the list')


def main():
    integer_list = []
    lock = threading.Lock()
    th1 = Producer(lock, integer_list)
    th2 = Consumer(lock, integer_list)
    th1.start()
    th2.start()


if __name__ == '__main__':
    main()
"""
整数每次产生都会被迅速消耗掉，消费者没有东西可以处理，但是依然不停地询问是否有东西可以处理（while True），这样不断地询问会比较浪费CPU等资源

integer list add integer 100
integer list lose integer 100
there is no integer in the list
there is no integer in the list
... 几百行一样的 ...
there is no integer in the list
integer list add integer 81
integer list lose integer 81
there is no integer in the list
there is no integer in the list
there is no integer in the list
......
"""
```

#### Condition
```python
import time
import threading
import random

class Producer(threading.Thread):

    def __init__(self, condition, integer_list):
        threading.Thread.__init__(self)
        self.condition = condition
        self.integer_list = integer_list

    def run(self):
        while True:
            random_integer = random.randint(0, 100)
            with self.condition:
                self.integer_list.append(random_integer)
                print(f'integer list add integer {random_integer}')
                self.condition.notify()
            time.sleep(1.2 * random.random())

class Consumer(threading.Thread):

    def __init__(self, condition, integer_list):
        threading.Thread.__init__(self)
        self.condition = condition
        self.integer_list = integer_list

    def run(self):
        while True:
            with self.condition:
                if self.integer_list:
                    integer = self.integer_list.pop()
                    print(f'integer list lose integer {integer}')
                    time.sleep(random.random())
                else:
                    print('there is no integer in the list')
                    self.condition.wait()

def main():
    integer_list = []
    condition = threading.Condition()
    th1 = Producer(condition, integer_list)
    th2 = Consumer(condition, integer_list)
    th1.start()
    th2.start()

if __name__ == '__main__':
    main()
"""
在生产出整数时notify通知wait的线程可以继续了
消费者查询到列表为空时调用wait等待通知（notify）

integer list add integer 7
integer list lose integer 7
there is no integer in the list
integer list add integer 98
integer list lose integer 98
there is no integer in the list
integer list add integer 84
integer list lose integer 84
.....
"""
```

#### 生产者与消费者的相互等待
上面是最基本的使用，下面我们多实现一个功能：生产者一次产生三个数，在列表数量大于5的时候停止生产，小于4的时候再开始

```python
import time
import threading
import random

class Producer(threading.Thread):

    def __init__(self, condition, integer_list):
        threading.Thread.__init__(self)
        self.condition = condition
        self.integer_list = integer_list

    def run(self):
        while True:
            with self.condition:
                if len(self.integer_list) > 5:
                    print('Producer start waiting')
                    self.condition.wait()
                else:
                    for _ in range(3):
                        self.integer_list.append(random.randint(0, 100))
                    print(f'now {self.integer_list} after add ')
                    self.condition.notify()
            time.sleep(random.random())

class Consumer(threading.Thread):

    def __init__(self, condition, integer_list):
        threading.Thread.__init__(self)
        self.condition = condition
        self.integer_list = integer_list

    def run(self):
        while True:
            with self.condition:
                if self.integer_list:
                    integer = self.integer_list.pop()
                    print(f'all {self.integer_list} lose {integer}')
                    time.sleep(random.random())
                    if len(self.integer_list) < 4:
                        self.condition.notify()
                        print("Producer don't need to wait")
                else:
                    print('there is no integer in the list')
                    self.condition.wait()

def main():
    integer_list = []
    condition = threading.Condition()
    th1 = Producer(condition, integer_list)
    th2 = Consumer(condition, integer_list)
    th1.start()
    th2.start()

if __name__ == '__main__':
    main()
```

#### Queue
queue模块内部实现了Condition，我们可以非常方便地使用生产者消费者模式

```python
"""
get方法会移除并赋值（相当于list中的pop），但是它在队列为空的时候会被阻塞（wait）
put方法是往里面添加值
如果想设置队列最大长度，初始化时这样做queue = Queue(10)指定最大长度，超过这个长度就会被阻塞（wait）
"""
import time
import threading
import random
from queue import Queue

class Producer(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            random_integer = random.randint(0, 100)
            self.queue.put(random_integer)
            print(f'add {random_integer}')
            time.sleep(random.random())

class Consumer(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            get_integer = self.queue.get()
            print(f'lose {get_integer}')
            time.sleep(random.random())

def main():
    queue = Queue()
    th1 = Producer(queue)
    th2 = Consumer(queue)
    th1.start()
    th2.start()

if __name__ == '__main__':
    main()
```
#### ListQueue
```python
"""
首先ListQueue类的构造：因为Queue类的源代码中，put是调用了_put，get调用_get，_init也是一样，所以我们重写这三个方法就将数据存储的类型和存取方式改变了。而其他部分锁的设计都没有变，也可以正常使用。改变之后我们就可以通过调用self.myqueue.queue来访问这个列表数据
"""
import time
import threading
import random
from queue import Queue

# 为了能查看队列数据，继承Queue定义一个类
class ListQueue(Queue):

    def _init(self, maxsize):
        self.maxsize = maxsize
        self.queue = [] # 将数据存储方式改为list

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.pop()

class Producer(threading.Thread):

    def __init__(self, myqueue):
        threading.Thread.__init__(self)
        self.myqueue = myqueue

    def run(self):
        while True:
            for _ in range(3): # 一个线程加入3个，注意：条件锁时上在了put上而不是整个循环上
                self.myqueue.put(random.randint(0, 100))
            print(f'now {self.myqueue.queue} after add ')
            time.sleep(random.random())

class Consumer(threading.Thread):

    def __init__(self, myqueue):
        threading.Thread.__init__(self)
        self.myqueue = myqueue

    def run(self):
        while True:
            get_integer = self.myqueue.get()
            print(f'lose {get_integer}', 'now total', self.myqueue.queue)
            time.sleep(random.random())

def main():
    queue = ListQueue(5)
    th1 = Producer(queue)
    th2 = Consumer(queue)
    th1.start()
    th2.start()

if __name__ == '__main__':
    main()

```
#### Event
```python
import threading
import time

class MyThread(threading.Thread):

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.event = event

    def run(self):
        print('first')
        self.event.wait()
        print('after wait')

event = threading.Event()
MyThread(event).start()
print('before set')
time.sleep(1)
event.set()
"""
可以看到结果

first
before set
先出现，1s之后才出现

after wait
"""
```