from celery.schedules import crontab

from app.constans import S_TYPE_TURNOVER
from app.statistics import insert_current_month_statistics
from . import celery, BaseTask, json_logger


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每天统计营业额
    sender.add_periodic_task(
        crontab(hour=1, minute=25),
        period_statistics_turnover_of_day.s(),
    )
    # 每月统计营业额
    sender.add_periodic_task(
        crontab(hour=1, minute=35, day_of_month=1),
        period_statistics_turnover_of_month.s(),
    )


@celery.task(name='period_statistics_turnover_of_day',
             base=BaseTask)
def period_statistics_turnover_of_day():
    """每天营业额统计任务"""
    print('每天营业额统计任务')
    json_logger.info('每天营业额统计任务')


@celery.task(name='period_statistics_turnover_of_month',
             base=BaseTask)
def period_statistics_turnover_of_month():
    """每月营业额统计任务"""
    # 在数据库中获取当月的数据，计算后创建月统计数据
    json_logger.info('每月营业额统计任务')

    insert_current_month_statistics(S_TYPE_TURNOVER)
