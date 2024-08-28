# tests.py
import pytest
from .model import OrderLine, Batch, Allocation
from datetime import date

@pytest.mark.django_db
class TestOrderLineModel:

    def test_orderline_model_can_load_lines(self):
        OrderLine.objects.bulk_create([
            OrderLine(orderid="order1", sku="RED-CHAIR", qty=12),
            OrderLine(orderid="order1", sku="RED-TABLE", qty=13),
            OrderLine(orderid="order2", sku="BLUE-LIPSTICK", qty=14),
        ])
        assert OrderLine.objects.count() == 3

    def test_orderline_model_can_save_lines(self):
        OrderLine.objects.create(orderid="order1", sku="DECORATIVE-WIDGET", qty=12)
        assert OrderLine.objects.count() == 1

@pytest.mark.django_db
class TestBatchModel:

    def test_retrieving_batches(self):
        Batch.objects.bulk_create([
            Batch(reference="batch1", sku="sku1", _purchased_quantity=100, eta=None),
            Batch(reference="batch2", sku="sku2", _purchased_quantity=200, eta=date(2011, 4, 11)),
        ])
        assert Batch.objects.count() == 2

    def test_saving_batches(self):
        Batch.objects.create(reference="batch1", sku="sku1", _purchased_quantity=100, eta=None)
        assert Batch.objects.count() == 1

@pytest.mark.django_db
class TestAllocationModel:

    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        self.batch = Batch.objects.create(reference="batch1", sku="sku1", _purchased_quantity=100, eta=None)
        self.line = OrderLine.objects.create(orderid="order1", sku="sku1", qty=10)

    def test_saving_allocations(self):
        Allocation.objects.create(orderline=self.line, batch=self.batch)
        assert Allocation.objects.count() == 1

    def test_retrieving_allocations(self):
        Allocation.objects.create(orderline=self.line, batch=self.batch)
        allocated_batch = Batch.objects.get(allocations__orderid="order1")
        assert allocated_batch.allocations.filter(sku="sku1").exists()
