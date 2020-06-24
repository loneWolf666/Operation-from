# -*- coding: utf-8 -*-
# Author: WangChao


import logging
import time

import redis

from app.public import PublicApp
from app.receive import ReceiveApp
from env.server import mqtt_server, redis_server
from env.topic_config import mqtt_topic_options
from libs.excepts import *

logger = logging.getLogger()


class App(object):

    def __init__(self):
        mqtt_server.on_connect = self.mqtt_on_connect
        mqtt_server.on_disconnect = self.mqtt_on_disconnect
        mqtt_server.loop_start()
        time.sleep(3)
        try:
            self.receive_app = ReceiveApp()
            self.public_app = PublicApp()
        except redis.exceptions.ConnectionError as ex:
            logger.warning('redis connect error, reconnecting......')
            self.set_redis_fail()
            self.retry_connect()
            logger.warning('redis reconnect success')
        except ExceptionError as ex:
            logger.error(ex)
        except ExceptionWarning as ex:
            logger.warning(ex)
        except ExceptionInfo as ex:
            logger.info(ex)
        except Exception as ex:
            logger.exception(ex)

    def retry_connect(self):
        """Redis 断链重试"""
        while True:
            try:
                redis_server.ping()
                self.set_redis_succeed()
            except:
                time.sleep(5)

    def set_redis_succeed(self):
        """set 状态 成功"""
        self.is_run = True
        logger.info('redis connect success')

    def set_redis_fail(self):
        """set 状态 失败"""
        self.is_run = True
        logger.info('redis connect fail')

    def mqtt_on_disconnect(self, client, user_data, rc):
        """MQTT 断开事件"""
        logger.error('mqtt disconnect rc=%s' % rc)
        self.public_app.app.is_run = False

    def mqtt_on_connect(self, client, user_data, flags, rc):
        """MQTT 链接事件"""
        topic_qos_list = [tuple(topic_qos.values()) for topic_qos in list(mqtt_topic_options.get('subscribe_topic').values())]
        mqtt_server.subscribe(topic_qos_list)
        self.public_app.app.is_run = True
