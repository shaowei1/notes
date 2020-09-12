import signal
import os


def do_exit(sig, stack):
    raise SystemExit('Exiting')


# 要忽略信号，请注册 SIG_IGN 为处理程序

signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGUSR1, do_exit)

print('My PID:', os.getpid())
# 等待接收信号
signal.pause()

# output
# My PID: 72598
# ^C^C^C^CExiting

"""
通常 SIGINT（当用户按下 Ctrl-C 时由 shell 发送到程序的信号）会引发 KeyboardInterrupt。
这个例子在它看到 SIGINT 时直接忽略了。输出中的每个 ^C 表示尝试从终端终止脚本。
从另一个终端使用 kill -USR1 72598 将脚本退出
"""
