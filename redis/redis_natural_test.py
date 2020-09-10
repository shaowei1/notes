import shutil
from concurrent.futures.process import ProcessPoolExecutor

import redis
import time

# strict connect
# r = redis.Redis(host='localhost', port= 6379)
hostname = '127.0.0.1'

# create redis connection use pool
pool = redis.ConnectionPool(host=f'{hostname}', port=6379)
r = redis.StrictRedis(connection_pool=pool)


# r = redis.Redis(connection_pool=pool)
def write():
    # 记录当前时间
    time1 = time.time()
    # 1 万次写
    for i in range(10000):
        data = {'username': 'zhangfei', 'age': 28}
        r.hmset("users" + str(i), data)
    # 统计写时间
    delta_time = time.time() - time1
    print(f'1 万次写: {delta_time}')
    # 统计当前时间


def read():
    time1 = time.time()
    # 1 万次读
    for i in range(10000):
        result = r.hmget("users" + str(i), ['username', 'age'])
    # 统计读时间
    delta_time = time.time() - time1
    print(f'1 万次读: {delta_time}')


def batch_write():
    time1 = time.time()
    # 批量写入
    pipe = r.pipeline()
    for i in range(10000):
        data = {'username': 'pipename', 'age': 18}
        pipe.hmset("users" + str(i), data)
        # pipe.delete("users" + str(i))
        # if i % 500 == 0:
        #     pipe.execute()

    resp = pipe.execute()
    print(resp)
    # 统计读时间
    delta_time = time.time() - time1
    print(f'1 万次批量写入: {delta_time}')


def try_pipeline():
    start = time.time()
    with r.pipeline(transaction=False) as p:
        p.sadd('seta', 1).sadd('seta', 2).srem('seta', 2).lpush('lista', 1).lrange('lista', 0, -1)
        p.execute()
    print(time.time() - start)


def worker():
    while True:
        try_pipeline()


def pool_run():
    with ProcessPoolExecutor(max_workers=12) as executor:
        for _ in range(10):
            future = executor.submit(worker)
            future.result()


if __name__ == '__main__':
    # pool_run()
    batch_write()
# 1 万次写: 0.7409350872039795
# 1 万次读: 0.6769979000091553
# 1 万次批量写入: 0.2712891101837158
