from django.contrib import admin

from pedidos.admin_actions import make_published
from pedidos.models import Item, Order, OrderItem

from django_admin_row_actions import AdminRowActionsMixin


class OrderItemStacked(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    list_display = ['__str__', 'total', 'status']
    actions = [make_published, ]
    inlines = [OrderItemStacked, ]

    def get_form(self, request, obj=None, change=False, **kwargs):
        """ User and Status should be prefilled and invisible, except for superusers """
        form = super().get_form(request, obj=obj, change=change, **kwargs)

        if not request.user.is_superuser:
            form.base_fields['user'].initial = request.user.pk
            form.base_fields['status'].initial = 'd'
            form.base_fields['user'].disabled = True
            form.base_fields['status'].disabled = True
        return form

    def get_queryset(self, request):
        """ Show for each user only his orders, except for superusers """
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_row_actions(self, obj):
        """ Add to each Order in OrderAdmin list individual actions """
        row_actions = [
            {
                'label': 'Enviar',
                'action': 'send',
                'enabled': obj.status is not 's',
            },
            {
                'label': 'Descargar .csv',
                'action': 'download',
                'enabled': True,
            },
        ]
        row_actions += super(OrderAdmin, self).get_row_actions(obj)
        return row_actions
