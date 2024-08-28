from django.db import models
from datetime import date

class OrderLine(models.Model):
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    orderid = models.CharField(max_length=255)

    def __str__(self):
        return f'OrderLine {self.orderid} - {self.sku}'

class Batch(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    sku = models.CharField(max_length=255)
    _purchased_quantity = models.IntegerField()
    eta = models.DateField(null=True, blank=True)
    allocations = models.ManyToManyField(OrderLine, through='Allocation', related_name='allocated_batches')

    def __str__(self):
        return f'Batch {self.reference} - {self.sku}'

class Allocation(models.Model):
    orderline = models.ForeignKey(OrderLine, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['orderline', 'batch']]

    def __str__(self):
        return f'Allocation {self.orderline} -> {self.batch}'
