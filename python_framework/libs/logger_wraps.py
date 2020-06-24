# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Date : 2019/11/14 11:12
import logging
import sys

from functools import wraps
from env import json_logger
from libs.excepts import ExceptionError

logger = logging.getLogger(__name__)


class Logger:
    """
    logger 装饰器
    """

    @staticmethod
    def local_logger(name=None, level="DEBUG"):
        """"""
        def print_logger(func):
            @wraps(func)
            def exec_func(*args, **kwargs):
                func_name = name
                if func_name is None:
                    file_line = sys._getframe().f_back.f_lineno
                    file_name = sys._getframe().f_code.co_filename
                    func_name = ":".join([file_name[0: -3], str(file_line)])
                log_func = getattr(logger, level.lower())
                log_func("{} - start".format(func_name))
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logger.error("{} - error".format(func_name))
                    raise ExceptionError(e)
                log_func("{} - end".format(func_name))
                return result
            return exec_func
        return print_logger

    @staticmethod
    def cloud_logger(name=None, level="DEBUG"):
        """"""
        def print_logger(func):
            @wraps(func)
            def exec_func(*args, **kwargs):
                func_name = name
                if func_name is None:
                    file_line = sys._getframe().f_back.f_lineno
                    file_name = sys._getframe().f_code.co_filename
                    func_name = ":".join([file_name[0: -3], str(file_line)])
                log_func = getattr(logger, level.lower())
                json_log = getattr(json_logger, level.lower())
                log_func("{} - start".format(func_name))
                json_log("{} - start".format(func_name))
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logger.error("{} - error".format(func_name))
                    json_logger.error("{} - error".format(func_name))
                    raise ExceptionError(e)
                log_func("{} - end".format(func_name))
                json_log("{} - end".format(func_name))
                return result
            return exec_func
        return print_logger
