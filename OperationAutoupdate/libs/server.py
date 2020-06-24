# -*- coding: utf-8 -*-
# Intro: Server Call
# Author: Ztj
# Version: 1.0.0
# Date: 2019-04-12

import logging

import paho.mqtt.client as mqtt
import pymysql
import redis
from DBUtils.PooledDB import PooledDB

logger = logging.getLogger()


def link_log(prefix, options):
    log_str = '%s: %s' % (prefix, options)
    password_str = "'password': %s" % options.get('password') if options.get(
        'password') is None else "'password': '%s'" % options.get('password')
    return log_str.replace(password_str, "'password': '******'")


def get_mysql_server(mysql_options):
    """获取 MySQL 服务"""
    logger.debug(link_log('link_mysql_server', mysql_options))
    mysql_pool = PooledDB(
        creator=pymysql,
        cursorclass=pymysql.cursors.DictCursor,
        **mysql_options
    )
    return mysql_pool, mysql_pool.connection()


def get_redis_server(redis_options):
    """获取 Redis 服务"""
    logger.debug(link_log('link_redis_server', redis_options))
    pool = redis.ConnectionPool(**redis_options, decode_responses=True)
    return redis.Redis(connection_pool=pool)


def get_mqtt_server(mqtt_options):
    """获取 MQTT 服务"""
    logger.debug(link_log('link_mqtt_server', mqtt_options))
    mqtt_server = mqtt.Client(
        mqtt_options.get('client_id'),
        bool(mqtt_options.get('clean_session', False)),
        mqtt_options.get('user_data', None),
    )
    mqtt_server.username_pw_set(
        mqtt_options.get('username', None),
        mqtt_options.get('password', None),
    )
    mqtt_server.connect(
        mqtt_options.get('host', '127.0.0.1'),
        int(mqtt_options.get('port', 1883)),
        int(mqtt_options.get('keep_alive', 60)),
        mqtt_options.get('bind_address', ''),
    )
    return mqtt_server
