# Django ORM models
from django.db import models

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    notes = models.TextField(blank=True, null=True)
