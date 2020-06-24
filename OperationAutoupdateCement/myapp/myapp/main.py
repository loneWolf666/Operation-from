from __future__ import absolute_import, unicode_literals
import sys


sys.path.append('../../')
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from myapp.myapp.controllers.items import Items
from myapp.myapp.core.exc import MyAppError
from myapp.myapp.controllers.base import Base
from myapp.myapp.controllers.autoupdate import AutoUpdate

import os
from tinydb import TinyDB
from cement.utils import fs

from celery import Celery


celery_app = Celery(main='myapp',
                    broker='amqp://redis://127.0.0.1:6379',
                    backend='amqp://redis://127.0.0.1:6379',
                    )


def extend_tinydb(app):
    app.log.info('extending todo application with tinydb')
    db_file = app.config.get('todo', 'db_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.info('tinydb database file is: %s' % db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


# configuration defaults
CONFIG = init_defaults('myapp')
CONFIG['myapp']['foo'] = 'bar'
CONFIG['myapp']['db_file'] = '~/.myapp/db.json'


class MyApp(App):
    """My Application primary application."""

    class Meta:
        label = 'myapp'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Items,
            AutoUpdate,
        ]


class MyAppTest(TestApp, MyApp):
    """A sub-class of MyApp that is better suited for testing."""

    class Meta:
        label = 'myapp'


def main():
    with MyApp() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except MyAppError as e:
            print('MyAppError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
