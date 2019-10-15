import csv
from io import StringIO

from django.core.mail import EmailMessage
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.db import models

from django.utils.text import slugify

from ZapatosBernini.settings import SENDORDER_MAIL


class Order(models.Model):
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('s', 'Sent'),
    ]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

    @property
    def total(self):
        """ Calculates the total cost of the order """
        return sum([item.total for item in self.items.all()])

    def generate_csv(self):
        """ Generates the .csv with the information of the Order """
        orderitems = self.items.all()

        with StringIO() as string_csv:
            writer = csv.writer(string_csv, delimiter=';')

            # First row
            writer.writerow(
                ['#', 'Item', 'Qty', 'Price', 'Total'],
            )

            # Contents
            for position, orderitem in enumerate(orderitems, start=1):
                item = orderitem.item
                writer.writerow(
                    [position, item.name, orderitem.qty, item.price, orderitem.total]
                )

            # End rows
            writer.writerow(
                ['', '', '', 'TOTAL', sum([o.total for o in orderitems])],
            )

            return string_csv.getvalue()

    def download(self):
        """ Downloads an Order as a .csv """
        return HttpResponse(self.generate_csv(), content_type='text/csv')

    def send(self):
        """ Generates and sends an email with Order details as .csv """
        def do_send(order, csv_as_str):
            subject = body = f'{order} from {order.user}'
            message = EmailMessage(
                subject=subject,
                body=body,
                from_email=SENDORDER_MAIL,
                to=[SENDORDER_MAIL, ],
            )
            filename = f'{slugify(order)}.csv'
            message.attach(filename, csv_as_str, 'text/csv')
            message.send()

        str_csv = self.generate_csv()
        do_send(self, str_csv)
        self.status = 's'
        self.save()

    def __str__(self):
        return f"Order #{self.pk}"


class Item(models.Model):
    """ Represents a product item """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} ({self.price})'


class OrderItem(models.Model):
    SIZES = (
        ('36', 36),
        ('38', 38),
        ('40', 40),
        ('42', 42),
        ('44', 44),
        ('46', 46),
        ('48', 48),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    size = models.CharField(max_length=2, choices=SIZES)
    qty = models.IntegerField()

    @property
    def total(self):
        """ Calculates total line cost i.e.: quantity * price """
        return self.qty * self.item.price

    def __str__(self):
        return f'{self.item.name} -> {self.order}'
