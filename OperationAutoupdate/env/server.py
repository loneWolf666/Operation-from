# -*- coding: utf-8 -*-
# Author: Ztj

import logging

from registry import Registry

from libs.excepts import ExceptionService
from libs.server import get_mysql_server, get_redis_server, get_mqtt_server
from . import GlobalConfigFile, app_options

logger = logging.getLogger()

"""获取服务配置"""
server_options = Registry(GlobalConfigFile.load_app('server'))

"""初始化 MySQL 服务"""
mysql_enable = app_options.get('server.mysql_enable', False)
mysql_options = server_options.get('mysql_server')
if mysql_enable is True:
    if mysql_options is None:
        raise ExceptionService('MySQL 配置为 None')
    mysql_pool, mysql_server = get_mysql_server(mysql_options)
    mysql_server.ping()

"""初始化 Redis 服务"""
redis_enable = app_options.get('server.redis_enable', False)
redis_options = server_options.get('redis_server')
if redis_enable is True:
    if redis_options is None:
        raise ExceptionService('Redis 配置为 None')
    redis_server = get_redis_server(redis_options)
    redis_server.ping()

"""初始化 MQTT 服务"""
mqtt_enable = app_options.get('server.mqtt_enable', False)
mqtt_options = server_options.get('mqtt_server')
if mqtt_enable is True:
    if mqtt_options is None:
        raise ExceptionService('MQTT 配置为 None')
    service_alias = '%s_%s' % (app_options.get('service.name', 'unknown'), app_options.get('service.id', '0'))
    mqtt_options['client_id'] = str(mqtt_options.get('client_id') or service_alias)
    mqtt_server = get_mqtt_server(mqtt_options)
