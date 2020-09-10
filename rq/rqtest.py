import time
from rq import Queue
from redis import Redis
from somewhere import count_words_at_url

# 告诉RQ连接哪个Redis
redis_conn = Redis()  # 默认连接localhost:6319
q = Queue(name='low_rq_test', connection=redis_conn)  # 默认队列没有使用其他参数

# 延迟执行count_words_at_url函数
job = q.enqueue(count_words_at_url, "https://www.baidu.com/")
# q.enqueue_call(func=count_words_at_url, args=(‘http://nvie.com’), timeout=30)

print(job.result)  # => None

# 现在，等待一会儿，直到worker完成
time.sleep(5)
print(job.result)
