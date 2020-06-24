from libs.listen import RedisQueueListenParse
from .tasks.task_event import revoke_task, trade_complete
from time import time
from env.server import redis_server


class EventHandler(RedisQueueListenParse):

    def __init__(self):
        super().__init__()
        self.parse_callback = self.handle_event_tasks
        self.redis_queue_key = 'event:'
        self.redis_server = redis_server
        self.data_to_json = True

    def run(self):
        self.listen()

    def push_task_id(self, key, task_id):
        # 记录 task_id 和 instance_id
        # 取消任务时，可以通过 instance_id 找到 task
        self.redis_server.rpush(key, task_id)

    def get_task_ids(self, key):
        # 取出 instance_id  下全部 task_id
        task_ids = self.redis_server.lrange(key, 0, -1)

        return task_ids

    def delete_tasks(self, key):
        """删除任务"""
        self.redis_server.ltrim(key, 0, 0)
        self.redis_server.rpop(key)

    def trade_complete(self, data):
        """订单完成后，执行任务"""
        event_type = data.get('event_type')

        # FIXME 定时时间需要计算
        eta = time.now()
        # TODO 先查看是否已有订单已经完成的任务，保证不会重复创建任务
        task = trade_complete(data, eta=eta)

        task_id = task.id
        instance_id = data.get()
        key = '{}:{}'.format(event_type, instance_id)

        self.push_task_id(key, task_id)

    def cancel_order(self, data):
        """取消订单后，执行任务"""
        event_type = data.get('event_type')
        trade_id = data.get('trade_id')
        key = '{}:{}'.format(event_type, trade_id)

        task_ids = self.get_task_ids(key)
        revoke_task(task_ids)
        self.delete_tasks(key)

    def handle_event_tasks(self, data):
        """处理事件"""
        event_type = data.get('event_type')
        consumers = {
            'trade_complete': self.trade_complete,
            'cancel_order': self.cancel_order,
        }
        consumer_func = consumers.get(event_type)
        if consumer_func:
            consumer_func(data)
