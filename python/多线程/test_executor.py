# 异步执行可以由 ThreadPoolExecutor 使用线程或由 ProcessPoolExecutor 使用单独的进程来实现。 两者都是实现抽像类 Executor 定义的接口。
from concurrent.futures.thread import ThreadPoolExecutor
import shutil

with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(pow, 323, 1235)
    executor.submit(shutil.copy, 'src1.txt', 'dest1.txt')
    print(future.result())

