# models.py
from django.db import models
from datetime import date

class OrderLine(models.Model):
    orderid = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()

class Batch(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    sku = models.CharField(max_length=255)
    _purchased_quantity = models.IntegerField()
    eta = models.DateField(null=True, blank=True)
    allocations = models.ManyToManyField(OrderLine, through='Allocation')

class Allocation(models.Model):
    orderline = models.ForeignKey(OrderLine, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
