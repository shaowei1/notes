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
