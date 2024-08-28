
# tests.py
import pytest
from django.utils import timezone
from datetime import timedelta
from .model import OrderLine, Batch
from .allocation import allocate, OutOfStock

@pytest.mark.django_db
class TestAllocation:
    
    def test_allocates_to_batch_with_available_stock(self):
        batch = Batch.objects.create(reference='batch1', sku='RETRO-CLOCK', _purchased_quantity=100, eta=timezone.now().date())
        line = OrderLine.objects.create(orderid='order1', sku='RETRO-CLOCK', qty=10)
        
        allocate(line, [batch])

        assert batch.available_quantity == 90

    def test_prefers_current_stock_batches_to_shipments(self):
        in_stock_batch = Batch.objects.create(reference="in-stock-batch", sku="RETRO-CLOCK", _purchased_quantity=100, eta=None)
        shipment_batch = Batch.objects.create(reference="shipment-batch", sku="RETRO-CLOCK", _purchased_quantity=100, eta=timezone.now().date() + timedelta(days=1))
        line = OrderLine.objects.create(orderid="oref", sku="RETRO-CLOCK", qty=10)

        allocation_ref = allocate(line, [in_stock_batch, shipment_batch])

        assert allocation_ref == in_stock_batch.reference

    def test_raises_out_of_stock_exception_if_cannot_allocate(self):
        batch = Batch.objects.create(reference="batch1", sku="SMALL-FORK", _purchased_quantity=10, eta=timezone.now().date())
        line = OrderLine.objects.create(orderid="order1", sku="SMALL-FORK", qty=10)
        allocate(line, [batch])

        with pytest.raises(OutOfStock):
            new_line = OrderLine.objects.create(orderid="order2", sku="SMALL-FORK", qty=1)
            allocate(new_line, [batch])
