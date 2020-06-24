from env.server import redis_server
from libs.excepts import *
from libs.listen import RedisQueueListenParse
import redis
import json
import time

from libs.listen import logger

"""
需要redis自带的两个方法（lrange, ltrim）

"""
class RedisQueueListenParsePipeline(RedisQueueListenParse):
    """重载框架数据解析"""

    def listen(self):
        """监听执行"""
        last_check_run_time = 0
        while self.is_run:
            if self.redis_state is False:
                self.reconnect()
                continue

            cur_time = int(time.time())

            if self.parse() is None and (cur_time - last_check_run_time) > (10 * 60):
                logger.debug('queue is empty, the program is running......')
                last_check_run_time = cur_time
                redis_server.lrange()

    def parse(self):
        """解析数据"""
        if self.redis_queue_key is None:
            raise ExceptionService('redis list key is None')
        if self.parse_callback is None:
            raise ExceptionService('parse callback is None')

        # 获取队列
        try:
            key = self.redis_queue_key
            queue_len = 1000 if redis_server.llen(key) > 1000 else redis_server.llen(key)
            with redis_server.pipeline(transaction=False) as pipe:
                for _ in range(queue_len):
                    pipe.rpop(key)
                data = pipe.execute()
        except redis.exceptions.ResponseError:
            raise ExceptionService('Redis get data error, redis key is not list. ||| %s' % self.redis_queue_key)
        except redis.exceptions.ConnectionError:
            self.redis_state = False
            return False

        # 开始解析数据
        if not data:
            time.sleep(self.parse_sleep)
            return None
        else:
            logger.debug('ParseData: %s' % data)

        # 解析 Json 数据
        try:
            data = json.loads(data) if self.data_to_json else data
        except:
            logger.exception('json data parse error, Please check if it is json string. ||| %s' % data)
            return False

        # 回调执行
        try:
            return self.parse_callback(data)
        except ExceptionError as ex:
            logger.error(ex)
        except ExceptionWarning as ex:
            logger.warning(ex)
        except ExceptionInfo as ex:
            logger.info(ex)
