# -*- coding: utf-8 -*-
# Intro: Redis 队列监听解析模块
# Author: Ztj
# Version: 1.0.0
# Date: 2019-04-22
# Assoc: excepts


import json
import logging
import time
import redis

from .excepts import ExceptionError, ExceptionWarning, ExceptionInfo, ExceptionService

logger = logging.getLogger(__name__)


class RedisQueueListenParse(object):
    """Redis 队列监听解析"""

    def __init__(self):
        self.is_run = True
        self.redis_state = True
        self.emq_state = True
        self.redis_queue_key = None
        self.parse_callback = None
        self.redis_server = None
        self.data_to_json = False
        self.parse_sleep = 5

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

    def reconnect(self):
        """重连"""
        try:
            self.redis_server.ping()
            self.redis_state = True
            logger.info('redis reconnect success')
        except:
            logger.warning('redis reconnect failure')
            time.sleep(10)

    def parse(self):
        """解析数据"""
        if self.redis_queue_key is None:
            raise ExceptionService('redis list key is None')
        if self.parse_callback is None:
            raise ExceptionService('parse callback is None')

        # 获取队列
        try:
            if self.emq_state is True:
                data = self.redis_server.rpop(self.redis_queue_key)
            else:
                time.sleep(10)
                return
        except redis.exceptions.ResponseError:
            raise ExceptionService('Redis get data error, redis key is not list. ||| %s' % self.redis_queue_key)
        except redis.exceptions.ConnectionError:
            self.redis_state = False
            return False

        # 开始解析数据
        if data is None:
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
