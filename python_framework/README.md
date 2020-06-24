异步任务
======
# 事件任务
- 流程图：https://www.processon.com/view/link/5ed9be23e401fd691957f284
- 解析事件，根据事件类型创建任务。任务可以为异步任务、定时任务、延时任务。

## celery 任务队列
- 文档： http://docs.jinkan.org/docs/celery/getting-started/introduction.html

## 创建任务
```rdoc
在 app.tasks 目录下创建任务文件，以 task_ 开头

```

## 异步任务
```rdoc
调用者调用此任务后，任务会被发送到 broker 队列中
任务消费方得到任务后，处理任务
```

## 延时任务
```rdoc
调用任务时，传入参数 countdown （单位是秒）后，
此任务就会在指定时间后执行 
```

## 定时任务
```rdoc
在应用启动信号后，添加定时任务调度

也可以通过以下方式添加
celery.conf.beat_schedule = {
    'add': {
        'task': 'add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
```

## 启动 celery 服务
```shell script
# 启动 worker
celery -A app.celery_config worker -l info

# 有定时或者周期性任务时，使用celery beat作为任务调度器
celery -A app.celery_config beat -l info

# 同时启动 worker 和 beat 
# 如果你永远不会运行一个以上的worker节点，这很方便，但是它并不常用，因此不建议用于生产环境
# https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
celery -B -A app.celery_config worker -l info

```

## 测试
- 执行测试: make test
