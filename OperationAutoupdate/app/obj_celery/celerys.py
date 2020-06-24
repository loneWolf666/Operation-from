from __future__ import absolute_import, unicode_literals
import sys
sys.path.append('./')
print(sys.path)
from celery import Celery

celery_app = Celery('obj_celery',
             broker='amqp://redis://127.0.0.1:6379',
             backend='amqp://redis://127.0.0.1:6379',
             include=['obj_celery.tasks'])

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery_app.start()
