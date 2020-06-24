from env import json_logger
from . import auto_delay, celery, BaseTask


@auto_delay
@celery.task(name='revoke_task', base=BaseTask)
def revoke_task(task_ids):
    for task_id in task_ids:
        celery.control.revoke(task_id)
    json_logger.info('revoke tasks: {}'.format(task_ids))


@auto_delay
@celery.task(name='trade_complete', base=BaseTask)
def trade_complete(trade_id):
    # 创建订单完成后的一系列任务
    json_logger.info('trade complete: {}'.format(trade_id))
