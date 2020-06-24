from celery.schedules import crontab

from app.constans import S_TYPE_INCOME
from app.statistics import insert_current_month_statistics
from . import celery, BaseTask, json_logger


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每天统计收入
    sender.add_periodic_task(
        crontab(hour=1, minute=20),
        period_statistics_income_of_day.s(),
    )
    # 每月统计收入
    sender.add_periodic_task(
        crontab(hour=1, minute=30, day_of_month=1),
        period_statistics_income_of_month.s(),
    )


@celery.task(name='period_statistics_income_of_day',
             base=BaseTask)
def period_statistics_income_of_day():
    """每天收入统计任务"""
    json_logger.info('每天收入统计任务')
    print('每天收入统计任务')


@celery.task(name='period_statistics_income_of_month',
             base=BaseTask)
def period_statistics_income_of_month():
    """每月收入统计任务"""
    json_logger.info('每月收入统计任务')
    insert_current_month_statistics(S_TYPE_INCOME)
