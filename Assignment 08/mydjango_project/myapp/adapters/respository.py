# Repository interface and implementation
from myapp.domain import models as domain_models
from . import orm

class BookmarkRepository:
    def add(self, title, url, notes):
        orm_bookmark = orm.Bookmark(title=title, url=url, notes=notes)
        orm_bookmark.save()
        return domain_models.Bookmark(title=title, url=url, notes=notes)
