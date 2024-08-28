# Dependency Injection and system bootstrap
from myapp.service_layer import message_bus, command_handlers
from myapp.adapters import orm

def bootstrap():
    orm.start_mappers()
    bus = message_bus.MessageBus({
        command_handlers.CreateBookmarkCommand: command_handlers.add_bookmark_handler,
    })
    return bus
