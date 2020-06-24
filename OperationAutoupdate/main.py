# -*- coding: utf-8 -*-
# Author: Ztj


from argtools import command, argument
from env import app_options


@command
@argument('--service_id', dest='service_id', help='service id', default='dev')
def listen(args=None):
    app_options.set('service.id', args.service_id)

    from app import App
    App()


@command.add_sub(name='ping_server', help='ping server')
@argument('--service_id', dest='service_id', help='service id', default='test')
def ping_server(args=None):
    app_options.set('service.id', args.service_id)

    from env.server import mysql_server, redis_server

    redis_server.ping()
    mysql_server.ping()


if __name__ == '__main__':
    command.run()
