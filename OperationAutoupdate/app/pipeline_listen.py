from env.server import redis_server
from libs.excepts import *
from libs.listen import RedisQueueListenParse
import redis
import json
import time

from libs.listen import logger

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

    def parse(self):
        """解析数据"""
        len_num = 10
        if self.redis_queue_key is None:
            raise ExceptionService('redis list key is None')
        if self.parse_callback is None:
            raise ExceptionService('parse callback is None')

        # 获取队列
        try:
            with redis_server.pipeline(transaction=False) as pipe:
                pipe.multi()
                pipe.lrange(self.redis_queue_key, 0 - len_num, -1)
                pipe.ltrim(self.redis_queue_key, 0, 0 - len_num)
                data = pipe.execute()
        except redis.exceptions.ResponseError:
            pipe.reset()
            raise ExceptionService('Redis get data error, redis key is not list. ||| %s' % self.redis_queue_key)
        except redis.exceptions.ConnectionError:
            self.redis_state = False
            return False

        # 开始解析数据
        if not data or len(data[0]) == 0:
            time.sleep(self.parse_sleep)
            return None
        else:
            logger.debug('ParseData: %s' % data)

        # 解析 Json 数据
        if data[1] == False:
            logger.exception('json data parse error, Please check if it is json string. ||| %s' % data)
            return False
        data = data[0]
        try:
            data = data if isinstance(data, list) else json.loads(data)
        except:
            logger.exception('json data parse error, Please check if it is json string. ||| %s' % data)
            return False

        # 回调执行
        try:
            self.parser_pipe(data)
        except ExceptionError as ex:
            logger.error(ex)
        except ExceptionWarning as ex:
            logger.warning(ex)
        except ExceptionInfo as ex:
            logger.info(ex)

    def parser_pipe(self, data_list):
        """解析队列数据"""
        for data in data_list:
            data = json.loads(data) if self.data_to_json else data
            self.parse_callback(data)
