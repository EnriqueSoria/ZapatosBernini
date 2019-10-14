from django.contrib.auth.models import User
from django.db import models


STATUS_CHOICES = [
    ('d', 'Draft'),
    ('s', 'Sent'),
]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

    def __str__(self):
        return f"Order #{self.pk}"


class Item(models.Model):
    SIZES = (
        ('36', 36),
        ('38', 38),
        ('40', 40),
        ('42', 42),
        ('44', 44),
        ('46', 46),
        ('48', 48),
    )

    name = models.CharField(max_length=200)
    size = models.PositiveSmallIntegerField(choices=SIZES)
    description = models.CharField(max_length=4000)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} ({self.price})'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self):
        return f'{self.item.name} -> {self.order}'
