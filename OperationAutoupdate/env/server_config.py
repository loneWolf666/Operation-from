# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Author : "ShiWeiDong"
# Date : 2019/4/17 12:13:35
from registry import Registry

from . import GlobalConfigFile

"""获取接口选项"""
server_options = Registry(GlobalConfigFile.load_app('server'))
