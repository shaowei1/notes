# recv_signal.py
"""
首先启动程序（根据打印的 pid），
在另外的窗口输入 kill -1 21838 和 kill -HUP 21838, 最后使用 ctrl+c关闭程序
"""
import signal
import time
import sys
import os


def handle_int(sig, frame):
    print(f"get signal: {sig}, I will quit")
    sys.exit(0)


def handle_hup(sig, frame):
    print(f"get signal: {sig}")


if __name__ == "__main__":
    signal.signal(2, handle_int)
    signal.signal(1, handle_hup)
    print(f"My pid is {os.getpid()}")
    while True:
        time.sleep(3)

# output
# My pid is 21838
# get signal: 1
# get signal: 1
# ^Cget signal: 2, I will quit
