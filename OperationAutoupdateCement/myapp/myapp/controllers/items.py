from time import strftime, time
from cement import Controller, ex

class Items(Controller):
    class Meta:
        label = 'items'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='list items')
    def list(self):
        pass

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