# -*- coding: utf-8 -*-
# Intro: 共用异常处理模块
# Author: Ztj
# Version: 1.1.0
# Date: 2019-04-12
# Assoc: excepts


class ExceptionBase(Exception):
    """基础异常"""
    pass


class ExceptionService(ExceptionBase):
    """服务异常"""
    pass


class ExceptionServer(ExceptionBase):
    """服务异常"""
    pass


class ExceptionError(ExceptionBase):
    """错误异常"""
    pass


class ExceptionWarning(ExceptionBase):
    """警告异常"""
    pass


class ExceptionInfo(ExceptionBase):
    """消息异常"""
    pass
