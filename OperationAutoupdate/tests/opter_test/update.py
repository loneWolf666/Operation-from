# -*- coding: utf-8 -*-
# Author: WangChao
# Version: 更新数据
# Version:  click 实现命令行接口
# click-7.1.2

import sys

sys.path.append('../..')
import click
import time
from env.server import redis_server
from env.topic_config import mqtt_topic_options


@click.command()
@click.option('--api', default=1.0, help='Api version. 接口版本')
@click.option('--timestamp', default=time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())),
              help='Timestamp. 时间戳')
@click.option('--ver', prompt='Operation-related ver', help='Ver version. 协议版本')
@click.option('--cmd', prompt='Operation-related cmd', help='Operation-related cmd')
@click.option('--id', prompt='Operation-related id', help='Operation-related id')
@click.option('--dn', prompt='Operation-related dn', help='Operation-related dn')
@click.option("-data_file", type=click.File("rb"), help='Operation-related data_file')
@click.option("-data_path", type=click.Path(exists=True), required=True, help='Operation-related data_path')
def update_dev(api, timestamp, cmd, ver, id, dn, data_file, data_path):
    """
    Upgrade the command line interface
        -- 更新交互
    """
    click.secho('API %s!' % api, bg='green', fg='red')
    click.secho('Timestamp %s!' % timestamp, bg='green', fg='red')
    with open(data_path, mode='r') as f:
        conext = f.read()
        name = mqtt_topic_options.get('update_list.from_list')
        redis_server.lpush(name, conext)
        click.secho(conext, fg='green')



if __name__ == '__main__':
    update_dev()
