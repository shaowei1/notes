import time
from concurrent.futures.thread import ThreadPoolExecutor


def dead_lock1():
    def wait_on_b():
        time.sleep(5)
        print(b.result())  # b will never complete because it is waiting on a.
        return 5

    def wait_on_a():
        time.sleep(5)
        print(a.result())  # a will never complete because it is waiting on b.
        return 6

    executor = ThreadPoolExecutor(max_workers=2)
    a = executor.submit(wait_on_b)
    b = executor.submit(wait_on_a)


def dead_lock2():
    def wait_on_future():
        f = executor.submit(pow, 5, 2)
        # todo 为什么没有执行到
        # This will never complete because there is only one worker thread and
        # it is executing this function.
        print(f.result())

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(wait_on_future)


if __name__ == '__main__':
    # dead_lock1()
    dead_lock2()
