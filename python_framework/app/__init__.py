from .event import EventHandler


def create_app():
    app = EventHandler()
    return app
