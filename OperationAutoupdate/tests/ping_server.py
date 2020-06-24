# -*- coding: utf-8 -*-
# Author: Ztj

from env.server import mysql_server, redis_server, mqtt_server

redis_server.ping()
mysql_server.ping()
mqtt_server.reconnect()
