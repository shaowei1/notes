import redis
import threading

hostname = '192.168.15.179'

# 创建连接池
pool = redis.ConnectionPool(host=f'{hostname}', port=6379)

# 初始化 redis
r = redis.StrictRedis(connection_pool=pool)

# 设置 KEY
KEY = "ticket_count"


# 模拟第 i 个用户进行抢票
def sell(i):
    # 初始化 pipe
    pipe = r.pipeline()
    while True:
        try:
            # 监视票数
            pipe.watch(KEY)
            # 查看票数
            c = int(pipe.get(KEY))
            if c > 0:
                # 开始事务
                pipe.multi()
                c = c - 1
                pipe.set(KEY, c)
                pipe.execute()
                print('用户 {} 抢票成功，当前票数 {}'.format(i, c))
                break
            else:
                print('用户 {} 抢票失败，票卖完了'.format(i))
                break
        except Exception as e:
            # print(e)  # Watched variable changed
            print('用户 {} 抢票失败，重试一次'.format(i))
            continue
        finally:
            pipe.unwatch()


if __name__ == "__main__":
    # 使用WATCH + MULTI 实现乐观锁, redis 不存在悲观锁
    # 初始化 5 张票
    r.set(KEY, 5)
    # 设置 8 个人抢票
    for i in range(8):
        t = threading.Thread(target=sell, args=(i,))
        t.start()
