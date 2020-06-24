# -*- coding: utf-8 -*-
# Author: WangChao
# Version: 更新数据


from time import strftime
from cement import Controller, ex
from myapp.myapp.main import celery_app
@celery_app.tasks
def add(x, y):
    return x + y

class AutoUpdate(Controller):
    class Meta:
        label = 'autoupdate'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='celery tasks add ',
        arguments=[
            ['num'],
            {'help': 'num',
             'action': 'store'}
        ]
        )
    def celery_add(self):
        num = self.app.pargs.num
        add.delay(num, 4)


    @ex(
        help='create an item',
        arguments=[
            (['item_text'],
             {'help': 'todo item text',
              'action': 'store'})
        ],
    )
    def create(self):
        text = self.app.pargs.item_text
        print(f'-------------{text}')
        now = strftime("%Y-%m-%d %H:%M:%S")
        self.app.log.info('creating todo item: %s' % text)

        item = {
            'timestamp': now,
            'state': 'pending',
            'text': text,
        }

        self.app.db.insert(item)

    @ex(help='update an existing item')
    def update(self):
        pass

    @ex(help='delete an item')
    def delete(self):
        pass

    @ex(help='complete an item')
    def complete(self):
        pass

    @ex(help='autoupdate an device  自动更新')
    def autoupdate(self):
        pass
