def make_published(modeladmin, request, queryset):
    for order in queryset:
        order.send()


make_published.short_description = "Send selected orders"
