import os
from kombu import Queue, Exchange
from celery import Celery

CELERY_VISIBILITY_TIMEOUT = 60 * 60 * 10


class CeleryConfig:
    broker_url = os.getenv('BROKER_URL',
                           'redis://localhost:6379')
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    task_default_queue = 'event'
    task_queues = [
        Queue('event', exchange=Exchange('direct'),
              routing_key='event.#')
    ]
    broker_transport_options = {
        'visibility_timeout': CELERY_VISIBILITY_TIMEOUT,
    }
    timezone = 'Asia/Shanghai'


def get_tasks(file_dir, file_prefix):
    front_path = file_dir.replace('/', '.')
    return [front_path + file.split('.')[0]
            for file in os.listdir(file_dir) if file.startswith(file_prefix)]


def make_celery():
    tasks = get_tasks('app/tasks/', 'task_')
    celery_ = Celery('app', include=tasks)

    celery_.config_from_object(CeleryConfig)

    return celery_


celery = make_celery()
