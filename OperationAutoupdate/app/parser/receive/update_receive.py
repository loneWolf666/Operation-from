# -*- coding: utf-8 -*-
# Author: WangChao
# Versions: 设备更新

import json
import logging
import os

import requests
import hashlib
from app.pipeline_listen import RedisQueueListenParsePipeline
from env.server import redis_server
from env.topic_config import mqtt_topic_options

logger = logging.getLogger('__name__')
bind_topic = mqtt_topic_options.get('alert_topic.public_topic')
mod_active = True


class Callback:

    def options(self):
        self.app = RedisQueueListenParsePipeline()
        self.app.redis_queue_key = 'Queue:list:second'
        self.app.is_parser_listen = True
        self.app.parse_callback = self.handle
        self.app.data_to_json = True
        self.app.parse_sleep = 0.3

    def handle(self, data):
        print(data, '*&*' * 20)

    @staticmethod
    def exec(**kwargs):
        """
        kwargs  topic -- data
        data    topic  payload
        payload  api dn json data
        """
        logger.info('MQTT 接收解析器 测试参数获取{}'.format(kwargs))
        topic = kwargs.get('topic', bind_topic)
        msg = kwargs.get('data', dict())
        payload = msg.get('payload')
        payload_data = payload.get('data')
        if payload_data:
            opkg_url = payload_data.get('opkg_url')
            if opkg_url:
                opkg = requests.get(opkg_url)
                md5hash = hashlib.md5(opkg.content)
                md5 = md5hash.hexdigest()
                print(f'字节流{md5}')
        qos = payload.get('qos', dict())
        dn = payload.get('dn')
        redis_server.hmset(name='AntoUpdate:Subscribe:{}'.format(dn),
                           mapping=dict(subscribe='1',
                                        payload=json.dumps(kwargs)
                                        ))
        logger.debug("Topic - [{}] - Msg - [{}] - Qos - [{}].".format(topic, msg, qos))
        redis_server.lpush(mqtt_topic_options.get('update_list.to_list'), json.dumps(kwargs))
        logger.debug("-------------------------- receive end ---------------------------------")
