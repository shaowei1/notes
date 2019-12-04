import json
import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "2")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
num_threads_str = os.getenv("NUM_THREADS", "2")
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "80")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores + 1
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = int(default_web_concurrency)

num_threads = int(num_threads_str)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
threads = num_threads
bind = use_bind
errorlog = "-"

# Access log with X-Forwarded-For
accesslog = "-"
access_log_format = '%({x-forwarded-for}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
forwarded_allow_ips = "*"

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "threads": threads,
    "bind": bind,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
}

print(json.dumps(log_data))
