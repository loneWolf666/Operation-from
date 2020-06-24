import json
import time

from env.server import redis_server, logger

num = 5


def set_pub():
    name = 'Queue:alert:error:list'
    dic = {
        "tag": ["order", "play", "parse"],
        "msg": "接收到开始播放事件",
        "data": {
            "trade_id": "YH20191210000063"
        },
        "datetime": "2019-12-10 17:51:20,979",
        "host": "ed21fd9bb5ca",
        "file_line": "event.py:35",
        "state": "receive_start_event",
        "level": "ERROR",
        "source": "Cloud-PlayParse",
        "alias": "order.info"
    }
    push_list = [json.dumps(dic) for _ in range(num)]
    try:
        logger.debug("=" * 10+ "执行启动时间 {}".format(int(str(time.time()).replace('.', '')))+"=" * 10)
        with redis_server.pipeline(transaction=False) as pipe:
            pipe.lpush(name, *push_list)
            pipe.execute()
    except Exception as e:
        logger.debug(e)


set_pub()
