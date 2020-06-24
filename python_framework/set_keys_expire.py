from argtools import command, argument

from env import app_options


@command.add_sub(name='set_keys_expire', help='set_keys_expire')
@argument('--service_id', dest='service_id', help='service id', default='dev')
@argument('--pattern', dest='pattern', help='pattern', default='test-key:*')
@argument('--second', dest='second', help='second', default=36000)
def set_keys_expire(args=None):
    app_options.set('service.id', args.service_id)
    iter_count = 500
    exec_count = 5000

    if args.pattern and args.second:
        from env.server import redis_server

        pipe = redis_server.pipeline()
        count = 0
        for key in redis_server.scan_iter(match=args.pattern,
                                          count=iter_count):
            count += 1
            pipe.expire(key, args.second)
            if count == exec_count:
                count = 0
                pipe.execute()


if __name__ == '__main__':
    command.run()
