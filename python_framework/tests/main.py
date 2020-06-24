# -*- coding: utf-8 -*-
# Author: Ztj

from argtools import command, argument

from env import app_options


@command
@argument('--service_id', dest='service_id', help='service id', default='dev')
def listen(args=None):
    app_options.set('service.id', args.service_id)


@command.add_sub(name='ping_server', help='ping server')
@argument('--service_id', dest='service_id', help='service id', default='dev')
def ping_server(args=None):
    app_options.set('service.id', args.service_id)

    from env.server import mysql_server, redis_server, mqtt_server

    redis_server.ping()
    mysql_server.ping()
    mqtt_server.reconnect()


@command.add_sub(name='set_keys_expire', help='set_keys_expire')
@argument('--service_id', dest='service_id', help='service id', default='dev')
@argument('--pattern', dest='pattern', help='pattern', default='test-key:*')
@argument('--second', dest='second', help='second', default=36000)
def set_keys_expire(args=None):
    app_options.set('service.id', args.service_id)

    if args.keys and args.second:
        from env.server import mysql_server, redis_server, mqtt_server

        keys = {}
        for i in range(100):
            keys['test-key:'+ str(i)] = 'value' + str(i)
        redis_server.mset(keys)

        pipe = redis_server.pipeline()
        for key in redis_server.scan_iter(match=args.pattern, count=10):
            pipe.expire(key, args.second)

        results = pipe.execute()
        print(results)


if __name__ == '__main__':
    command.run()
