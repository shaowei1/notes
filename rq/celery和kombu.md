# celery

> 1. 指定结果集 CELERY_RESULT_BACKEND， 指定任务集CELERY_BROKER_URL
> 2. 创建celery 对象
> 3. 给对象注册方法和指定队列
> 4. 启动多个worker消费者(worker轮训任务)，给CELERY_BROKER_URL 发送任务

```python3
from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.conf.redis_socket_keepalive = True

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(queue=f'{APP_NAMESPACE}:CELERY:task_name', soft_time_limit=SOFT_TIME_LIMIT)

```

- 启动命令

  ```shell
  
  celery -A engine.runserver.celery worker -l debug -Q MODULE_NAME:CELERY:task_name1,MODULE_NAME:CELERY:task_name2
  ```

  

## kombu

> 1. 

- 启动命令

  ```shell
  pip install kombu
  ```

  

