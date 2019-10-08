from django.contrib import admin

# Register your models here.
from pedidos.admin_actions import make_published
from pedidos.models import Item, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)

        if not request.user.is_superuser:
            form.base_fields['order'].queryset = Order.objects.filter(user=request.user)
        return form

    def get_queryset(self, request):
        qs = super(OrderItemAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(order__user=request.user)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'pk', 'status']
    actions = [make_published]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)

        if not request.user.is_superuser:
            form.base_fields['user'].initial = request.user.pk
            form.base_fields['status'].initial = 'd'
            form.base_fields['user'].disabled = True
            form.base_fields['status'].disabled = True
        return form

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
