# CQRS commands
class Command:
    pass

class CreateBookmarkCommand(Command):
    def __init__(self, title, url, notes):
        self.title = title
        self.url = url
        self.notes = notes
