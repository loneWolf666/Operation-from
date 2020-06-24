# -*- coding: utf-8 -*-
# Author: WangChao
# Versions: 设备更新
import hashlib
import json

import requests

from app.pipeline_listen import RedisQueueListenParsePipeline
from env.server import redis_server
from env.topic_config import mqtt_topic_options

mod_active = True
import logging

logger = logging.getLogger()


class Call(object):


    def options(self):
        self.app = RedisQueueListenParsePipeline()
        self.app.redis_queue_key = 'Queue:test:first'
        self.app.is_parser_listen = True
        self.app.parse_callback = self.handle
        self.app.data_to_json = True
        self.app.parse_sleep = 0.3

    def handle(self, data):
        print(data, '*&*' * 20)

    def exec(self, payload):
        logger.debug("推送测试测试数据 - {}".format(payload))
        data = payload.get('data')
        if data:
            opkg_url = data.get('opkg_url')
            if opkg_url:
                opkg = requests.get(opkg_url)
                md5hash = hashlib.md5(opkg.content)
                md5 = md5hash.hexdigest()
                print(f'字节流{md5}*********************************')
        dn = payload.get('dn')
        redis_server.hmset(name='AntoUpdate:Publish:{}'.format(dn),
                           mapping=dict(publish_state='1',
                                        payload=json.dumps(data),
                                        ))
        return dict(topic=mqtt_topic_options.get('update_topic.public_topic'), payload=payload)
