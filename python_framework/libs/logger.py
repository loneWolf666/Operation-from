# -*- coding: utf-8 -*-
# Author: Ztj

import logging
import json
import threading
from .excepts import ExceptionService


class JsonLogger(logging.Logger):
    extra = dict()
    local = threading.local()

    def add(self, **kwargs):
        if threading.current_thread().name == 'MainThread':
            self.extra.update(kwargs)
        else:
            for k, v in kwargs.items():
                self.local.__setattr__(k, v)
        return self

    def get(self, name):
        return self.get(name)

    def get_all(self):
        return dict(**self.extra, **self.local.__dict__)

    def handle(self, record):
        record.extra = self.get_all()
        super().handle(record)

    def set_source(self, source):
        self.add(source=source)
        return self

    def set_host(self, host):
        self.add(host=host)
        return self

    def set_tag(self, tag):
        self.add(tag=tag)
        return self

    def set_alias(self, alias):
        self.add(alias=alias)
        return self

    def set_state(self, state):
        self.add(state=state)
        return self

    def set_data(self, **kwargs):
        self.add(**kwargs)
        return self


class JsonFormatter(logging.Formatter):

    def format(self, record):
        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            extra = getattr(record, 'extra')
            isinstance(record.args, dict) and extra.update(record.args)
        else:
            raise ExceptionService('json formatter error, log record lose extra')

        tag = extra.pop('tag', 'unknown')
        tag = tag if isinstance(tag, list) else [tag]

        return str(json.dumps({
            "datetime": self.formatTime(record),
            "source": extra.pop('source', 'unknown'),
            "file_line": ':'.join([record.filename, str(record.lineno)]),
            "host": extra.pop('host', 'unknown'),
            "level": record.levelname,
            "msg": str(record.msg),
            "tag": tag,
            "alias": extra.pop('alias', 'unknown'),
            "state": extra.pop('state', 'unknown'),
            "data": extra
        }, ensure_ascii=False))
