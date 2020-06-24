import json
import logging
import time
from env.server import redis_server
logger = logging.getLogger('__name__')
bind_topic = "devfilmhouse/test/#"
mod_active = False

num = 0

class Callback:

    @staticmethod
    def exec(**kwargs):
        logger.info('MQTT 接收解析器 测试参数获取{}'.format(kwargs))
        global num
        num += 1
        initial = redis_server.hget('Service:Mqtt:Sub:Pub', 'sub_pub_time')
        data = {
            str(num): int(str(time.time()).replace('.', '')) - int(initial)
        }
        redis_server.hmset("Service:Mqtt:Sub:Pub", data)
        logger.debug("-------------------------- receive end ---------------------------------")


