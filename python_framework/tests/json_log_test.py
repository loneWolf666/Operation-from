import logging
import threading
import time

from env import json_logger

json_logger.info('啥都不填')

json_logger.add(source='PythonFramework')
json_logger.add(tag=['test'])
json_logger.add(host='0.0.0.0')

json_logger.info('这是一个全局日志', dict(alias='global', state='start', nas_id='a1'))


def worker(sleep, name):
    json_logger.add(name=name)
    time.sleep(sleep)
    json_logger.info('这是一个线程日志', dict(alias='thread', state=name, nas_id=str(threading.current_thread())))


t1 = threading.Thread(target=worker, args=(5, 'worker1',))
t1.start()

t2 = threading.Thread(target=worker, args=(1, 'worker2',))
t2.start()

t1.join()
t2.join()

json_logger.info('这是一个全局日志', extra=dict(alias='global', state='end'))

logger = logging.getLogger(__name__)

logger.info('这是一条常规日志')

