# -*- coding: utf-8 -*-
# Author: WangChao


import json
import logging
import time
import uuid
import redis

from env.server import mqtt_server
from env.server import redis_server
from libs.excepts import *
from libs.mods import DirMods

logger = logging.getLogger()


class ReceiveApp(object):
    is_run = True

    def __init__(self):

        self.parser = self.get_parser()
        mqtt_server.on_message = self.mqtt_on_message

    @staticmethod
    def get_parser():
        """获取解析器"""
        logger.debug('*' * 25 + ' parser ' + '*' * 25)
        dir_mods = DirMods('app.parser.receive')
        mods = dict()
        for name, mod in dir_mods.all().items():
            if not hasattr(mod, 'mod_active'):
                continue
            if not getattr(mod, 'mod_active'):
                continue
            if not hasattr(mod, 'bind_topic'):
                continue
            else:
                sign = getattr(mod, 'bind_topic').split("/")[1]
            if not hasattr(mod, 'Callback'):
                continue
            if not isinstance(mods.get(sign), dict):
                mods[sign] = dict()
            mods[sign][name] = getattr(mod, 'Callback')()
            logger.debug('load parser: %s - %s' % (sign, name))
        return mods

    def mqtt_on_message(self, client, user_data, msg):
        """消息接收"""
        topic = msg.topic
        payload = msg.payload.decode()
        qos = msg.qos
        self.exec(dict(sign=topic.split("/")[1], topic=topic, data=payload, qos=qos))

    def exec(self, item):
        """执行函数"""
        logger.debug('A' * 50)
        [logger.debug('%s - %s' % (k, v)) for k, v in item.items()]
        topic = item.get('topic')
        data = item.get('data')
        qos = item.get('qos')
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            logger.error('error：%s' % item)
            logger.debug('E' * 50)
            return False
        data = self.uuid_add(data=data)
        mods = self.parser.get(item.get('sign'), dict())
        for name, mod in mods.items():
            if hasattr(mod, 'exec'):
                self.callback(name, mod, topic, data, qos)

        logger.debug('Z' * 50)

    def uuid_add(self, data):
        """添加 uuid 缓存"""
        num = str(int(uuid.uuid1()))[:5]
        date = str(round(time.time() * 1000))
        mqtt_uuid = ''.join([date, num])
        data['mqtt_uuid'] = mqtt_uuid
        json_data = json.dumps(data)
        name = 'Cache:MqttReceive:{}'.format(mqtt_uuid)
        try:
            redis_server.setex(name=name, time=3600, value=json_data)
        except Exception as ex:
            logger.error('缓存唯一标识异常', ex)
        return data

    def callback(self, name, mod, topic, data, qos):
        """执行函数"""
        logger.debug('-' * 50)
        logger.debug('callback %s......' % name)
        uid = data.get('mqtt_uuid')
        logger.debug(
            "MQTT Receive - Topic - [{}] - Mqtt_uid- [{}]- Msg - [{}] - Qos - [{}].".format(topic, uid, data, qos))
        try:
            getattr(mod, 'exec')(topic=topic, data=data, qos=qos)
        except redis.exceptions.ConnectionError as ex:
            logger.warning('redis connect error, reconnecting......')
            self.is_run = False
            logger.warning('redis reconnect success')
            self.callback(name, mod, topic, data, qos)
        except ExceptionError as ex:
            logger.error(ex)
        except ExceptionWarning as ex:
            logger.warning(ex)
        except ExceptionInfo as ex:
            logger.info(ex)
        except Exception as ex:
            logger.exception(ex)
