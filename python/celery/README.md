导入模块时先从__init__,然后依次遍历导入的所有的模块，函数，有装饰器的函数略过


from celery import current_task is   celery.Task._app.current_worker_task.request
celery.Task._app.current_worker_task.request.x_request_id
args
timelimit


current_request_id.ctx_fetchers [flask_ctx_get_request_id, ctx_celery_task_get_request_id]

celery 通过 signals 提前插入 self.receivers 一些函数，可以在每次worker 前执行

@celery.task()  --> _create_task_cls
def func()      --> _create_task_cls(func) << add task to self.tasks, and bind
