# Command handlers
from myapp.adapters.repository import BookmarkRepository

def add_bookmark_handler(command):
    repo = BookmarkRepository()
    repo.add(command.title, command.url, command.notes)
