import time

from env.server import redis_server

mod_active = False
import logging

logger = logging.getLogger()

num = 0

class Call(object):
    def __init__(self):
        pass

    def exec(self, payload):
        logger.info("推送测试测试数据 - {}".format(payload))
        data = dict(sub_pub_time=int(str(time.time()).replace('.', '')))
        try:
            redis_server.hmset("Service:Mqtt:Sub:Pub", data)
        except Exception as e:
            logger.error("测试入队列失效数据异常 {}".format(e) * 20, e)
        logger.debug("-------------------------- public end ---------------------------------")
        return dict(topic='devfilmhouse/test', payload=payload)
