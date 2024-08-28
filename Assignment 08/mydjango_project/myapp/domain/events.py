# events.py

class Event:
    pass

class BookmarkCreated(Event):
    def __init__(self, id, title, url):
        self.id = id
        self.title = title
        self.url = url

class BookmarkDeleted(Event):
    def __init__(self, id):
        self.id = id

