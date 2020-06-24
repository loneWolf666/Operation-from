import json
import time

from env.server import redis_server, logger

num = 10


def set_pub():
    name = 'Queue:mqtt:public'
    dic = dict(
        topic='test',
        payload={
            "topic_cmd": "switch",
            "trade_id": "YH20191122000005",
            "publish_type": "single",
            "addr": 2,
            "publish_time": 1574412759,
            "type": "lock",
            "control_cmd": "switch_on",
            "gateway_id": "GAwg4hSuJ09r"
        }
    )
    push_list = [json.dumps(dic) for _ in range(num)]
    try:
        logger.debug("="*10,"执行启动时间 {}".format(int(str(time.time()).replace('.', ''))),"="*10)
        with redis_server.pipeline(transaction=False) as pipe:
            pipe.lpush(name, *push_list)
            pipe.execute()
    except Exception as e:
        logger.debug(e)



set_pub()
