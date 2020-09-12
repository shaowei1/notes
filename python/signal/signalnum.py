import signal


def handle_hup(sig, frame):
    print("get signal: %s" % sig)


signal.signal(1, handle_hup)

if __name__ == "__main__":

    ign = signal.SIG_IGN
    dfl = signal.SIG_DFL
    print("SIG_IGN", ign)
    print("SIG_DFL", dfl)
    print("*" * 40)

    for name in dir(signal):
        if name[:3] == "SIG" and name[3] != "_":
            signum = getattr(signal, name)
            # signal.getsignal 返回信号对应的 handler,
            # 可能是一个可以调用的 Python 对象，
            # 或者是 signal.SIG_IGN（表示被忽略）,
            # signal.SIG_DFL（默认行为已经被使用）
            # 或 None（Python 的 handler 还没被定义）
            gsig = signal.getsignal(signum)

            print(name, int(signum), gsig)

"""output
可以看到大部分信号都是都有默认的行为

SIG_IGN 1
SIG_DFL 0
****************************************
SIGABRT 6 0
SIGALRM 14 0
SIGBUS 10 0
SIGCHLD 20 0
SIGCONT 19 0
SIGEMT 7 0
SIGFPE 8 0
SIGHUP 1 <function handle_hup at 0x109371c80>
SIGILL 4 0
SIGINFO 29 0
SIGINT 2 <built-in function default_int_handler>
SIGIO 23 0
SIGIOT 6 0
SIGKILL 9 None
SIGPIPE 13 1
SIGPROF 27 0
SIGQUIT 3 0
SIGSEGV 11 0
SIGSTOP 17 None
SIGSYS 12 0
SIGTERM 15 0
SIGTRAP 5 0
SIGTSTP 18 0
SIGTTIN 21 0
SIGTTOU 22 0
SIGURG 16 0
SIGUSR1 30 0
SIGUSR2 31 0
SIGVTALRM 26 0
SIGWINCH 28 0
SIGXCPU 24 0
SIGXFSZ 25 1


"""