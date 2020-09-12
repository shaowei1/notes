# thread_signal.py
"""
多线程环境下使用信号，只有 main thread 可以设置 signal 的 handler，也只有它能接收到 signal.
下面用一个例子看看效果，在一个线程中等待信号，并从另一个线程发送信号。

Python 的 signal 模块要求，所有的 handlers 必需在 main thread 中注册，即使底层平台支持线程和信号混合编程。
即使接收线程调用了 signal.pause()，但还是没有接收到信号。
代码结尾处的 signal.alarm(2) 是为了唤醒接收线程的 pause()，否则接收线程永远不会退出。

"""
import signal
import threading
import os
import time


def usr1_handler(num, frame):
    print("received signal %s %s" % (num, threading.currentThread()))


signal.signal(signal.SIGUSR1, usr1_handler)


def thread_get_signal():
    # 如果在子线程中设置signal的handler 会报错
    # ValueError: signal only works in main thread
    # signal.signal(signal.SIGUSR2, usr1_handler)

    print("waiting for signal in", threading.currentThread())
    # sleep 进程直到接收到信号
    signal.pause()
    # 子线程接受不到信号，不执行 waiting done
    raise Exception("waiting done")


receiver = threading.Thread(target=thread_get_signal, name="receiver")
receiver.start()
time.sleep(0.1)


def send_signal():
    print("sending signal in ", threading.currentThread())
    os.kill(os.getpid(), signal.SIGUSR1)


sender = threading.Thread(target=send_signal, name="sender")
sender.start()
sender.join()

print('pid', os.getpid())
# 这里是为了让程序结束，唤醒 pause
signal.alarm(2)
receiver.join()

# output
# waiting for signal in <Thread(receiver, started 123145306509312)>
# sending signal in  <Thread(sender, started 123145310715904)>
# received signal 30 <_MainThread(MainThread, started 140735138967552)>
# pid 23188
# [1]    23188 alarm      python thread_signal.py
