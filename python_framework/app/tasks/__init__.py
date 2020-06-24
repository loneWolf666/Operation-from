from env import json_logger
from app.celery_config import CeleryConfig, celery


class BaseTask(celery.Task):
    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        json_logger.info('任务执行失败：task_id: {task_id} exc:{exc}'.format(
            task_id=task_id, exc=exc))
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


def auto_delay(func):
    def wrapper(*args, **kwargs):
        try:
            if not CeleryConfig.broker_url:
                return
            func.apply_async(*args, **kwargs)
        except Exception as e:
            json_logger.info('celery task exec error: {}'.format(e))

    return wrapper
