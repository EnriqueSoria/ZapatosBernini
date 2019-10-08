from django.core.mail import send_mail, EmailMessage
from django.utils.text import slugify

from ZapatosBernini.settings import SENDORDER_MAIL
from pedidos.models import OrderItem


class OrderSender:

    def __init__(self, order):
        self.order = order
        self.csv = self.generate_csv()

    def generate_csv(self):
        items = OrderItem.objects.filter(order=self.order)

        csv = f'{self.order}\n\n'
        csv += f'#;Item;Qty;Price;Total\n'

        total = 0

        for position, orderitem in enumerate(items, start=1):
            item = orderitem.item
            total += item.price * orderitem.qty
            csv += '''{position};{item};{qty};{price};{total};{endline}'''.format(
                position = position,
                item = item.name,
                qty = orderitem.qty,
                price=item.price,
                total=item.price * orderitem.qty,
                endline='\n'
            )

        csv += f"\n\n;;;TOTAL;{total}"

        return csv

    def send(self):
        subject = body = f'{self.order} from {self.order.user}'
        message = EmailMessage(
            subject=subject,
            body=body,
            from_email=SENDORDER_MAIL,
            to=[SENDORDER_MAIL, ],
        )
        filename = f'{slugify(self.order)}.csv'
        message.attach(filename, self.csv, 'text/csv')


def make_published(modeladmin, request, queryset):
    for order in queryset:
        order_mail = OrderSender(order)
        order_mail.send()
        order.status = 's'
        order.save()


make_published.short_description = "Send selected orders"
