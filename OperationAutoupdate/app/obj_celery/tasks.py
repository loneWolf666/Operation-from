from __future__ import absolute_import, unicode_literals

from app.obj_celery.celerys import celery_app


@celery_app.task
def add(x, y):
    return x + y

@celery_app.task
def mul(x, y):
    return x * y

@celery_app.task
def xsum(numbers):
    return sum(numbers)



