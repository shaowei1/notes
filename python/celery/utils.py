import celery
from celery import Celery
from flask_log_request_id import current_request_id
from flask_log_request_id.ctx_fetcher import ExecutedOutsideContext
from kombu.transport.virtual import exchange


def get_queue_name():
    if celery.current_task is None:
        return None
    return celery.current_task.queue


def get_request_id():
    for ctx_fetcher in current_request_id.ctx_fetchers:
        try:
            request_id = ctx_fetcher()
            if request_id is None:
                # 需要换成celery 对象 celery = make_celery(app)
                return celery.current_worker_task.request.id
            return request_id
        except AttributeError:
            continue
        except ExecutedOutsideContext:
            continue
    return None


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
