# repository.py
from .model import Batch

class DjangoRepository:
    def add(self, entity):
        entity.save()

    def get(self, reference):
        return Batch.objects.get(reference=reference)
