import time
import json

from env import app_options

app_options.set('service.id', 'test_publish')
app_options.set('server.redis_enable', False)

from env.server import mqtt_server


def set_receive():
    mqtt_server.publish('devfilmhouse/test',
    payload=json.dumps(dict(
        # topic='test',
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
        )), qos=0)
    # mqtt_server.publish('devfilmhouse/test', payload=json.dumps(dict(plyaer='payload-2')), qos=0)
    # mqtt_server.publish('devfilmhouse/test', payload=json.dumps(dict(plyaer='payload-3')), qos=0)

    time.sleep(3)
set_receive()


