from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = [
        "user",
        "payment_method",
        "payment_id",
        "status",
        "amount_paid",
        "date_created",
    ]
    filter = ["date_created"]


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [
        "user",
        "payment",
        "status",
        "order_id",
        "created_at",
        "updated_at",
    ]
    ordering = ["created_at"]
    filter_horizontal = ()


class OrderProductAdmin(admin.ModelAdmin):
    model = OrderProduct
    list_display = [
        "user",
        "order",
        "payment",
        "product",
        "variation",
        "created_at",
        "updated_at",
    ]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
