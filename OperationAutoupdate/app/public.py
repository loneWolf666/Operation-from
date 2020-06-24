# -*- coding: utf-8 -*-
# Author: WangChao

import json
import logging
import os
import time
import uuid

from app.pipeline_listen import RedisQueueListenParsePipeline
from env.server import mqtt_server
from env.server import redis_server
from env.topic_config import mqtt_topic_options
from libs.excepts import *
from libs.listen import RedisQueueListenParse
from libs.mods import DirMods

logger = logging.getLogger()


class PublicApp(object):
    is_listen = True

    def __init__(self):
        self.parser = self.get_parser()
        self.app = RedisQueueListenParsePipeline()
        self.app.redis_server = redis_server
        self.app.redis_queue_key = mqtt_topic_options.get('update_list.from_list')
        self.app.parse_callback = self.callback
        self.app.data_to_json = True
        self.app.parse_sleep = 0.3
        self.app.is_run = True

        while self.is_listen:
            self.app.listen()
            time.sleep(5)

    def callback(self, data):
        topic = data.get('topic', mqtt_topic_options.get('alert_topic.public_topic'))
        payload = data
        qos = data.get('qos', 1)
        mqtt_uuid = self.make_uuid()

        if topic is None:
            raise ExceptionError('topic not exist')
        else:
            logger.debug('topic: %s' % topic)

        if payload is None:
            raise ExceptionError('payload not exist')
        else:
            logger.debug('payload: %s' % payload)

        publish_list = list()
        # root_parser = self.parser.get('root').get('app.parser.public.' + topic)
        # sub_parser = self.parser.get('app.parser.public.' + topic)
        root_parser = self.parser.get('root').get('app.parser.public.'+'update_public')
        sub_parser = self.parser.get('app.parser.public.'+'update_public')
        if root_parser is None:
            publish_list.append(dict(topic=topic, payload=payload, qos=qos, mqtt_uuid=mqtt_uuid))
        elif not sub_parser:
            logger.debug('-' * 50)
            logger.debug('exec parser: %s' % 'app.parser.public.' + topic)
            publish_list.append(self.get_publish(root_parser, payload, qos, mqtt_uuid))
        else:
            payload = payload if not hasattr(root_parser, 'exec') else getattr(root_parser, 'exec')(payload)
            for name, mod in self.parser.get('root').items():
                if name == 'app.parser.public.' + 'update_public':
                # if name == 'app.parser.public.' + topic:  # todo 后期修改
                    logger.debug('-' * 50)
                    logger.debug('exec parser: %s' % name)
                    publish_list.append(self.get_publish(mod, payload, qos, mqtt_uuid))
        for publish in publish_list:
            if publish is None:
                continue

            topic = publish.get('topic')
            payload = publish.get('payload')
            qos = publish.get('qos', qos)
            mqtt_uuid = publish.get('mqtt_uuid')

            if topic is None or payload is None:
                continue

            logger.debug('-' * 50)
            logger.debug('publish topic: %s' % topic)
            logger.debug('publish payload: %s' % payload)
            logger.debug('publish qos: %s' % qos)
            payload = payload if isinstance(payload, str) else json.dumps(payload)
            mqtt_server.publish(topic, payload, qos)
            logger.debug("MQTT Public - Topic - [{}] - Mqtt_uid- [{}]- Payload - [{}] - Qos - [{}].".format(topic, mqtt_uuid, payload, qos))
            logger.debug("-------------------------- public end -------------------------------")

    @staticmethod
    def get_publish(mod, payload, qos, mqtt_uuid):
        if not hasattr(mod, 'exec'):
            return None
        data = getattr(mod, 'exec')(payload)

        if data is None:
            return None

        new_topic = data.get('topic')
        new_payload = data.get('payload')
        new_qos = data.get('qos', qos)

        logger.debug('new topic: %s' % new_topic)
        logger.debug('new payload: %s' % new_payload)
        logger.debug('new qos: %s' % new_qos)

        if new_topic is None or new_payload is None:
            return None

        return dict(topic=new_topic, payload=new_payload, qos=new_qos,mqtt_uuid=mqtt_uuid)

    @staticmethod
    def make_uuid():
        """添加 uuid 缓存"""
        num = str(int(uuid.uuid1()))[:5]
        date = str(round(time.time() * 1000))
        mqtt_uuid = ''.join([date, num])
        return mqtt_uuid

    @staticmethod
    def get_parser():
        """获取 public 解析器"""
        modules = dict()
        root_modules = DirMods('app.parser.public').filter('mod_active').call('Call')
        modules['root'] = root_modules
        for name, mod in root_modules.items():
            logger.debug('load public_parser: %s' % name)
            modules[name] = mod
            continue

        return modules
