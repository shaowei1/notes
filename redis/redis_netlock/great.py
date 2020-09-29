from redis.exceptions import LockError
import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)
try:
    with r.lock('my-lock-key', timeout=5, blocking_timeout=5) as lock:
        # code you want executed only after the lock has been acquired
        print('hello')
        time.sleep(10)
except LockError as e:
    # Cannot release a lock that's no longer owned
    # the lock wasn't acquired
    #  Unable to acquire lock within the time specified
    print(f'lock Error: {e}')
    pass
