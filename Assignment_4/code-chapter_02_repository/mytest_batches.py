# tests.py
import pytest
from django.utils import timezone
from datetime import timedelta
from .model import Batch, OrderLine

@pytest.fixture
def make_batch_and_line(db):
    def _make_batch_and_line(sku, batch_qty, line_qty):
        batch = Batch.objects.create(reference="batch-001", sku=sku, _purchased_quantity=batch_qty, eta=timezone.now().date())
        line = OrderLine.objects.create(orderid="order-123", sku=sku, qty=line_qty)
        return batch, line
    return _make_batch_and_line

@pytest.mark.django_db
class TestBatchModel:

    def test_allocating_to_a_batch_reduces_the_available_quantity(self, db):
        batch = Batch.objects.create(reference="batch-001", sku="SMALL-TABLE", _purchased_quantity=20, eta=timezone.now().date())
        line = OrderLine.objects.create(orderid="order-ref", sku="SMALL-TABLE", qty=2)

        batch.allocate(line)

        assert batch.available_quantity == 18

    def test_can_allocate_if_available_greater_than_required(self, make_batch_and_line):
        large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
        assert large_batch.can_allocate(small_line)

    def test_cannot_allocate_if_available_smaller_than_required(self, make_batch_and_line):
        small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
        assert not small_batch.can_allocate(large_line)

    def test_can_allocate_if_available_equal_to_required(self, make_batch_and_line):
        batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
        assert batch.can_allocate(line)

    def test_cannot_allocate_if_skus_do_not_match(self, db):
        batch = Batch.objects.create(reference="batch-001", sku="UNCOMFORTABLE-CHAIR", _purchased_quantity=100, eta=None)
        different_sku_line = OrderLine.objects.create(orderid="order-123", sku="EXPENSIVE-TOASTER", qty=10)
        assert not batch.can_allocate(different_sku_line)

    def test_allocation_is_idempotent(self, make_batch_and_line):
        batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
        batch.allocate(line)
        batch.allocate(line)
        assert batch.available_quantity == 18

    def test_deallocate(self, make_batch_and_line):
        batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
        batch.allocate(line)
        batch.deallocate(line)
        assert batch.available_quantity == 20

    def test_can_only_deallocate_allocated_lines(self, make_batch_and_line):
        batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
        batch.deallocate(unallocated_line)
        assert batch.available_quantity == 20
