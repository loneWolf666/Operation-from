# -*- coding: utf-8 -*-
# Author: Ztj

import logging
import logging.config
import os

from configfile import ConfigFile
from registry import Registry
from libs.logger import JsonLogger

"""全局设置"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

"""全局变量"""
service_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""初始化配置"""
GlobalConfigFile = ConfigFile(os.path.join(service_root_path, 'configs'))

"""加载配置文件"""
app_options = Registry(GlobalConfigFile.load_app('app'))

"""配置日志"""
log_options = GlobalConfigFile.load_app('log')
if log_options is not None:
    logging.setLoggerClass(JsonLogger)
    logging.config.dictConfig(log_options)

json_logger = logging.getLogger('json')
