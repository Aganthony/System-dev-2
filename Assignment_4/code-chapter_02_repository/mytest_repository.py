# tests.py
import pytest
from .model import Batch, OrderLine
from .repository import DjangoRepository

@pytest.mark.django_db
class TestRepository:

    def test_repository_can_save_a_batch(self):
        batch = Batch(reference="batch1", sku="RUSTY-SOAPDISH", _purchased_quantity=100, eta=None)
        repo = DjangoRepository()
        repo.add(batch)

        saved_batch = Batch.objects.get(reference="batch1")
        assert saved_batch.sku == "RUSTY-SOAPDISH"
        assert saved_batch._purchased_quantity == 100
        assert saved_batch.eta is None

    def test_repository_can_retrieve_a_batch_with_allocations(self):
        batch = Batch.objects.create(reference="batch1", sku="GENERIC-SOFA", _purchased_quantity=100, eta=None)
        order_line = OrderLine.objects.create(orderid="order1", sku="GENERIC-SOFA", qty=12)
        batch.allocations.add(order_line)

        repo = DjangoRepository()
        retrieved = repo.get("batch1")

        assert retrieved.sku == "GENERIC-SOFA"
        assert retrieved._purchased_quantity == 100
        assert retrieved.allocations.filter(orderid="order1").exists()
