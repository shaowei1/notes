"""
它被用于在一定时间之后，向进程自身发送 SIGALRM 信号，这对于避免无限期地阻塞 I/O 操作或其他系统调用很有用。

在此示例中，调用 sleep() 被中断，但在信号处理后继续，因此sleep()返回后打印的消息显示程序执行时间与睡眠持续时间一样长
"""
import signal
import time


def receive_alarm(signum, stack):
    print('Alarm :', time.ctime())


# Call receive_alarm in 2 seconds
signal.signal(signal.SIGALRM, receive_alarm)
signal.alarm(2)

print('Before:', time.ctime())
time.sleep(4)
print('After :', time.ctime())

# output
# Before: Sat Apr 22 14:48:57 2017
# Alarm : Sat Apr 22 14:48:59 2017
# After : Sat Apr 22 14:49:01 2017
