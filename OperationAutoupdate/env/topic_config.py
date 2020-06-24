# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Author : "WangChao"
# Date : 2020/05/09 15:13:35
from registry import Registry

from . import GlobalConfigFile

"""MQTT 主题配置"""
mqtt_topic_options = Registry(GlobalConfigFile.load_app('mqtt_topic'))
