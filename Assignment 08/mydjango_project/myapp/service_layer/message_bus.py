# Simplified message bus
class MessageBus:
    def __init__(self, command_handlers):
        self.command_handlers = command_handlers

    def handle(self, command):
        handler = self.command_handlers[type(command)]
        handler(command)
